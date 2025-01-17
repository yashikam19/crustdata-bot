import os
from langchain_community.vectorstores import Chroma
from langchain.prompts import ChatPromptTemplate
from langchain_community.chat_models import ChatOpenAI

class Retriever:
    def __init__(self, chroma_path, embedding_function, model_name="gpt-4o-mini"):
        self.chroma_path = chroma_path
        self.embedding_function = embedding_function
        self.model_name = model_name
        self.api_key = os.environ.get("OPENAI_API_KEY")

    async def create_chain(self):
        prompt_text = """
        You are an expert API documentation assistant. Your role is to help users understand and work with the Crustdata API. Here is how you should approach each query:
        
        ### Response Guidelines

        1. For each query, you must:
        - Only discuss API endpoints that are explicitly mentioned in the provided context
        - Use exact curl commands and JSON payloads exactly as shown in the documentation
        - Include all relevant request parameters, key points, links/resources that are explicitly documented

        2. If information is not available:
        - Do not attempt to guess or create new endpoints or parameters

        3. Formatting and Style:
        - For error-related queries, provide the direct solution without unnecessary explanation.
        - Avoid using the word "context" in the answer. Refer to the "documentation" instead.

        Now, answer the following query based on the provided context and the chat history given below only:

        Context: {context}

        Chat History: {history}

        Query: {question}

        Answer:
        """
        # Create the prompt template and model
        prompt = ChatPromptTemplate.from_template(prompt_text)
        model = ChatOpenAI(model=self.model_name, api_key=self.api_key)

        # Execute the prompt
        runnable = prompt | model
        return runnable

    async def query_rag(self, query_text, store: dict, session_id, k=20, relevance_threshold=0.5):
        # Load the Chroma database
        db = Chroma(persist_directory=self.chroma_path, embedding_function=self.embedding_function)

        # Retrieve context using similarity search
        results = db.similarity_search_with_relevance_scores(query_text, k=k)

        # Check for valid results
        # if len(results) == 0 or results[0][1] < relevance_threshold:
        #     return "Unable to find matching results.", None

        # Combine context from matching documents
        context_text = "\n\n - -\n\n".join([doc.page_content for doc, _score in results])

        llm_chain = await self.create_chain()

        if session_id not in store:
            store[session_id] = []

        history = "\n".join(
            f"{role}: {content}"
            for message in store[session_id]
            for role, content in message.items()
        )

        answer = llm_chain.invoke({"context": context_text, "history": history, "question": query_text})
        # Extract response and sources
        response_text = answer.content

        store[session_id].append({"Human": query_text})
        store[session_id].append({"AI": response_text})
        sources = [doc.metadata.get("source", None) for doc, _score in results]

        # Format the response
        formatted_response = f"Response: {response_text}\n\nSources: {sources}"
        return formatted_response, response_text

    async def retrieve_context(self, query_text, k=10):
        db = Chroma(persist_directory=self.chroma_path, embedding_function=self.embedding_function)
        return db.similarity_search_with_relevance_scores(query_text, k=k)
