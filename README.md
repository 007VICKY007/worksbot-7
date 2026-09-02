# 🤖 RAG PDF Question-Answering Chatbot

An enterprise-grade **Retrieval-Augmented Generation (RAG)** PDF Question-Answering Chatbot built using **Python, Streamlit, LangChain (v1.x LCEL), OpenAI API, and ChromaDB**.

This application allows users to upload single or multiple PDF documents, automatically extracts and chunks document text, generates vector embeddings, stores them in ChromaDB, and delivers **conversational, history-aware responses** based on document context with source attribution.

---

## Conversational History & Context Retrieval

The system incorporates **conversational memory & question reformulation**:
1. **History-Aware Question Reformulation**: When a user asks follow-up questions referencing previous messages (e.g. *"What are its main applications?"* or *"Can you explain point 2 further?"*), the pipeline reformulates the follow-up question into a standalone query using the chat history before executing ChromaDB similarity search.
2. **Contextual LLM Generation**: Passes the full conversation history alongside retrieved document chunks into the LLM prompt to generate consistent answers across multiple turns.

---

## Key Features

- **Dynamic PDF Ingestion**: Upload any PDF document (handles large multi-page textbooks seamlessly).
- **Enterprise Modular Architecture**: Decoupled codebase separated into `config.py`, `prompt_templates.py`, `rag_pipeline.py`, and `app.py`.
- **Modern LangChain LCEL**: Built using LangChain Expression Language (`RunnablePassthrough`, `PromptTemplate`, `ChatOpenAI`, `StrOutputParser`).
- **History-Aware Retrieval**: Contextualizes follow-up questions using conversation history for similarity search.
- **Humanized & Grounded Responses**: Conversational, warm, and accurate answers generated strictly from retrieved context.
- **Source Attribution**: Displays exact PDF filenames, page numbers (1-indexed), and text snippets for full traceability.
- **Robust Error Handling**: Filters out blank or non-extractable pages, uses `chromadb.PersistentClient` to prevent SQLite lock errors, and uses batch insertions.

---

## Architecture & Workflow

```text
               ┌───────────────────────┐
               │     Uploaded PDFs     │
               └───────────┬───────────┘
                           │
                           ▼
               ┌───────────────────────┐
               │    PyPDFLoader &      │
               │ DirectoryLoader (PDF) │
               └───────────┬───────────┘
                           │
                           ▼
               ┌───────────────────────┐
               │ Text Chunking & Filter│
               │ (RecursiveSplitter)   │
               └───────────┬───────────┘
                           │
                           ▼
               ┌───────────────────────┐
               │  OpenAI Embeddings    │
               │ (text-embedding-3-sm) │
               └───────────┬───────────┘
                           │
                           ▼
               ┌───────────────────────┐
               │  ChromaDB Vector Store│
               │ (PersistentClient)    │
               └───────────┬───────────┘
                           │
               ┌───────────┴───────────┐
               │ Similarity Search (K) │ ◄─────── Standalone Question
               └───────────┬───────────┘          (Reformulated from History)
                           │ Top-K Chunks
                           ▼
               ┌───────────────────────┐
               │ Conversational Prompt │ ◄─────── Chat History
               └───────────┬───────────┘
                           │
                           ▼
               ┌───────────────────────┐
               │ OpenAI Chat LLM       │
               │ (gpt-4o-mini)         │
               └───────────┬───────────┘
                           │
                           ▼
               ┌───────────────────────┐
               │ Streamlit UI Display  │
               │ (Answer + Sources)    │
               └───────────────────────┘
```

---

## Project Structure

```text
RAG/
│
├── config.py             # System configuration, paths, and OpenAI model parameters
├── prompt_templates.py   # Question reformulation & conversational prompt templates
├── rag_pipeline.py       # Core RAG engine with history-aware retrieval & ChromaDB
├── app.py                # Streamlit web application frontend
├── requirements.txt      # Project dependencies
├── .env                  # Environment variables (OpenAI API key)
├── .env.example          # Template for environment variables
└── .gitignore            # Git ignore rules
```

---

## Prerequisites & Setup

### 1. Prerequisites
- Python `3.10+`
- OpenAI API Key

### 2. Installation Steps

1. **Navigate to project directory:**
   ```bash
   cd /Volumes/Personal/RAG
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure OpenAI API Key in `.env`:**
   ```env
   OPENAI_API_KEY=your_openai_api_key_here
   ```

---

## Running the Application

Launch the Streamlit server:

```bash
python3 -m streamlit run app.py
```

Access the application in your browser at:
👉 **`http://localhost:8501`**

---

## 💡 How to Use

1. **Upload Document**: In the sidebar, select one or multiple PDF documents.
2. **Process Document**: Click **⚡ Process PDF & Build Pipeline**. The app will extract, chunk, embed, and index your document.
3. **Ask Questions**: Type your question in the chat input box at the bottom.
4. **Inspect Sources**: Expand the **📚 View Retrieved Sources** section under any answer to see exact page numbers and retrieved document snippets.
5. **Reset / New Document**: Click **🔄 Upload New Document** in the sidebar anytime to wipe the index and upload fresh documents.

---

## 📄 License

This project is licensed under the MIT License.
# worksbot-7
