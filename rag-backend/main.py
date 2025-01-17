from fastapi import FastAPI, File, UploadFile, HTTPException
from helpers.process_chunk import ChunkProcessor
from fastapi.responses import JSONResponse
from helpers.retriever_helper import Retriever
from langchain_community.embeddings import OpenAIEmbeddings
import uvicorn
import os

app = FastAPI(
    title="Crustdata RAG API",
    description="API for querying Crustdata API documentation",
    version="1.0",
    docs_url="/crustdata/docs",
    openapi_url="/crustdata/openapi.json"
)

store={}
EMBEDDING_MODEL = "text-embedding-ada-002"
CHROMA_PATH = "crust_v5"
embedding_function = OpenAIEmbeddings(model=EMBEDDING_MODEL, api_key=os.environ.get("OPENAI_API_KEY"))

@app.get("/crustdata/healthcheck")
def healthcheck():
    return {"status": "ok"}


@app.post("/crustdata/ingest")
async def ingest_file(chroma_path: str, file: UploadFile = File(...)):
    if file.content_type != "text/plain":
        raise HTTPException(status_code=400, detail="Invalid file type. Only .txt files are allowed.")

    try:
        chunk_processor = ChunkProcessor(
            embeddings=embedding_function,
            chroma_path=chroma_path,
            chunk_size=2000,
            chunk_overlap=300,
        )

        content = (await file.read()).decode("utf-8")

        # Create chunks
        chunks = await chunk_processor.create_chunks(content)
        print(f"Created {len(chunks)} chunks from the uploaded file.")
        
        await chunk_processor.add_documents_to_chroma(chunks)

        return JSONResponse(
            status_code=200,
            content={
                "message": f"Successfully processed and added to the Chroma DB.",
                "chunks_count": len(chunks),
            },
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")
    
@app.get("/crustdata/document-count")
async def document_count(database: str):
    """
    FastAPI endpoint to check the number of documents in the Chroma database.
    
    Returns:
    - dict: A response containing the document count.
    """
    try:
        chunk_processor = ChunkProcessor(
            embeddings=embedding_function,
            chroma_path=database,
            chunk_size=1000,
            chunk_overlap=200,
        )
        count = await chunk_processor.get_document_count()
        return {"document_count": count}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching document count: {str(e)}")
    
    
@app.post("/crustdata/query/{session_id}")
async def query_rag(query: str, session_id: str):
    """
    Query the RAG system with a specific question.
    """
    try:
        rag_handler = Retriever(chroma_path=CHROMA_PATH, embedding_function=embedding_function)
        formatted_response, response_text = await rag_handler.query_rag(query_text=query, store=store, session_id=session_id)
        if response_text is None:
            raise HTTPException(status_code=404, detail="No matching results found.")
        return {
            "response": response_text,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error querying RAG: {str(e)}")

@app.post("/crustdata/search")
async def search_results(query: str, k: int = 10):
    try:
        retriever = Retriever(chroma_path=CHROMA_PATH, embedding_function=embedding_function)
        results = await retriever.retrieve_context(query_text=query, k=k)

        if not results:
            raise HTTPException(status_code=404, detail="No matching results found.")

        # Format results as a list of dictionaries
        formatted_results = [
            {"content": doc.page_content, "relevance_score": score}
            for doc, score in results
        ]
        return JSONResponse(
            status_code=200,
            content={"query": query, "results": formatted_results},
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving search results: {str(e)}")

@app.get("/crustdata/retrieve_chat_history/{session_id}")
async def retrieve_chat_history(session_id: str):
    try:
        if session_id not in store:
            raise HTTPException(status_code=404, detail="Chat history not found for the given session ID.")
        return {"status": "success", "message": "Chat history retrieved successfully.", "history": store[session_id]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error occurred: {str(e)}")

@app.delete("/crustdata/delete_chat_history/{session_id}")
async def delete_chat_history(session_id: str):
    try:
        if session_id not in store:
            raise HTTPException(status_code=404, detail="Chat history not found for the given session ID.")
        del store[session_id]
        return {"status": "success", "message": f"Chat history for session {session_id} deleted successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error occurred: {str(e)}")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8081, reload=True)