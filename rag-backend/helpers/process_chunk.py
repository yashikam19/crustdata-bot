import os
import shutil
import asyncio
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document
from langchain_community.vectorstores import Chroma


class ChunkProcessor:
    def __init__(self, embeddings, chroma_path, chunk_size=1000, chunk_overlap=200):
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,
            is_separator_regex=False,
        )
        self.embeddings = embeddings
        self.chroma_path = chroma_path

    async def create_chunks(self, content: str) -> list[Document]:
        return self.text_splitter.create_documents([content])

    async def add_documents_to_chroma(self, chunks: list[Document]) -> None:
        """
        Add new documents to the Chroma database and persist changes.

        Args:
            chunks (list[Document]): List of document chunks to add.
        """
        db = Chroma(persist_directory=self.chroma_path, embedding_function=self.embeddings)

        # Add documents asynchronously
        await asyncio.to_thread(db.add_documents, chunks)

        # Persist the database asynchronously
        await asyncio.to_thread(db.persist)
        print(f"Added {len(chunks)} new documents to {self.chroma_path}.")

    async def get_document_count(self) -> int:
        """
        Get the count of documents in the Chroma database.
        
        Returns:
            int: The number of documents in the Chroma database.
        """
        if not os.path.exists(self.chroma_path):
            raise FileNotFoundError(f"Chroma database not found at {self.chroma_path}.")

        db = Chroma(persist_directory=self.chroma_path, embedding_function=self.embeddings)

        # Get document count asynchronously
        count = await asyncio.to_thread(lambda: db._collection.count())
        return count

    async def delete_chroma_db(self) -> None:
        """
        Delete the Chroma database by removing its directory.
        """
        if os.path.exists(self.chroma_path):
            try:
                # Asynchronously delete the directory
                await asyncio.to_thread(shutil.rmtree, self.chroma_path)
                print(f"Deleted the Chroma database at {self.chroma_path}.")
            except Exception as e:
                print(f"Error deleting the database: {str(e)}")
        else:
            print(f"No database found at {self.chroma_path} to delete.")
