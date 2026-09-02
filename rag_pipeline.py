import os
import shutil
from pathlib import Path
from typing import List, Dict, Any, Optional
import chromadb

from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import Chroma
from langchain_core.output_parsers import StrOutputParser

from config import (
    UPLOAD_DIR,
    VECTOR_DB_DIR,
    EMBEDDING_MODEL,
    LLM_MODEL,
    DEFAULT_CHUNK_SIZE,
    DEFAULT_CHUNK_OVERLAP,
    DEFAULT_TEMPERATURE,
    DEFAULT_TOP_K,
)
from prompt_templates import get_humanized_prompt


class RAGPipeline:
    """End-to-End Modular RAG Pipeline with ChromaDB PersistentClient & OpenAI LCEL."""

    def __init__(
        self,
        pdf_path: Path = UPLOAD_DIR,
        persist_directory: Path = VECTOR_DB_DIR,
        chunk_size: int = DEFAULT_CHUNK_SIZE,
        chunk_overlap: int = DEFAULT_CHUNK_OVERLAP,
        temperature: float = DEFAULT_TEMPERATURE,
        top_k: int = DEFAULT_TOP_K,
        api_key: Optional[str] = None
    ):
        self.pdf_path = Path(pdf_path)
        self.persist_directory = Path(persist_directory)
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.temperature = temperature
        self.top_k = top_k
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")

        self.documents = []
        self.chunks = []
        self.vector_store = None
        self.retriever = None
        self.rag_chain = None

    def load_documents(self) -> List:
        """Step 1: Load PDF documents and filter out blank/empty pages."""
        if not self.pdf_path.exists():
            raise FileNotFoundError(f"PDF directory '{self.pdf_path}' does not exist.")

        pdf_files = list(self.pdf_path.glob("*.pdf"))
        if not pdf_files:
            raise ValueError("No PDF files were found in the upload directory.")

        loader = DirectoryLoader(
            str(self.pdf_path),
            glob="**/*.pdf",
            loader_cls=PyPDFLoader
        )
        raw_docs = loader.load()
        
        # Filter out empty or whitespace-only pages
        valid_docs = [doc for doc in raw_docs if doc.page_content and doc.page_content.strip()]

        if not valid_docs:
            raise ValueError(
                "No readable text could be extracted from the uploaded PDF. "
                "Please make sure your PDF contains selectable text (not scanned image-only PDFs)."
            )
        return valid_docs

    def chunk_documents(self, documents: List) -> List:
        """Step 2: Split extracted document text into chunks and validate non-emptiness."""
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
            separators=["\n\n", "\n", " ", ""]
        )
        raw_chunks = text_splitter.split_documents(documents)
        valid_chunks = [c for c in raw_chunks if c.page_content and c.page_content.strip()]

        if not valid_chunks:
            raise ValueError("No valid text chunks were generated from the document.")

        return valid_chunks

    def create_vector_store(self, chunks: List):
        """Step 3: Index document chunks using Chromadb PersistentClient with batching."""
        if not self.api_key:
            raise ValueError("OpenAI API Key is missing. Please configure OPENAI_API_KEY.")

        if not chunks:
            raise ValueError("Cannot create vector database with empty document chunks.")

        embeddings = OpenAIEmbeddings(
            model=EMBEDDING_MODEL,
            api_key=self.api_key
        )

        # Initialize Chromadb PersistentClient safely
        client = chromadb.PersistentClient(path=str(self.persist_directory))

        # Reset collection cleanly via API to avoid SQLite file lock errors
        collection_name = "pdf_rag"
        try:
            client.delete_collection(collection_name)
        except Exception:
            pass

        vector_store = Chroma(
            client=client,
            collection_name=collection_name,
            embedding_function=embeddings
        )

        # Batch insert chunks to safely handle large PDFs (e.g. 100+ pages)
        batch_size = 100
        for i in range(0, len(chunks), batch_size):
            batch = chunks[i : i + batch_size]
            vector_store.add_documents(batch)

        return vector_store

    def setup_retriever(self):
        """Step 4: Configure ChromaDB similarity retriever."""
        if not self.vector_store:
            raise ValueError("Vector store is not initialized.")

        self.retriever = self.vector_store.as_retriever(
            search_type="similarity",
            search_kwargs={"k": self.top_k}
        )

    def create_qa_chain(self):
        """Step 5: Construct humanized LCEL Runnable QA chain with OpenAI LLM."""
        if not self.api_key:
            raise ValueError("OpenAI API Key is missing.")

        llm = ChatOpenAI(
            model=LLM_MODEL,
            temperature=self.temperature,
            api_key=self.api_key
        )

        prompt = get_humanized_prompt()

        def format_docs(docs: List) -> str:
            return "\n\n".join(doc.page_content for doc in docs)

        self.rag_chain = (
            {"context": lambda x: format_docs(x["docs"]), "question": lambda x: x["question"]}
            | prompt
            | llm
            | StrOutputParser()
        )

    def initialize(self):
        """Run full end-to-end RAG pipeline initialization."""
        self.documents = self.load_documents()
        self.chunks = self.chunk_documents(self.documents)
        self.vector_store = self.create_vector_store(self.chunks)
        self.setup_retriever()
        self.create_qa_chain()

    def query(self, question: str) -> Dict[str, Any]:
        """Execute similarity search and generate humanized response."""
        if not self.retriever or not self.rag_chain:
            return {
                "answer": "The RAG Pipeline is not initialized yet. Please upload a PDF and process it.",
                "source_documents": []
            }

        question = question.strip()
        if not question:
            return {"answer": "Please provide a valid question.", "source_documents": []}

        # Step 1: Retrieve context chunks
        docs = self.retriever.invoke(question)

        if not docs:
            return {
                "answer": "I searched the uploaded document, but I could not find information relevant to your question.",
                "source_documents": []
            }

        # Step 2: Generate response from LLM using LCEL chain
        humanized_answer = self.rag_chain.invoke({"docs": docs, "question": question})

        return {
            "answer": humanized_answer,
            "source_documents": docs
        }
