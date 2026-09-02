# 🤖 RAG PDF Question-Answering Chatbot

An enterprise-grade **Retrieval-Augmented Generation (RAG)** PDF Question-Answering Chatbot built using **Python, Streamlit, LangChain (v1.x LCEL), OpenAI API, and ChromaDB**.

This application allows users to upload single or multiple PDF documents (including large textbooks), automatically extracts and chunks document text, generates vector embeddings, stores them in ChromaDB, and delivers **humanized, grounded answers** based strictly on the document context with full source attribution.

---

## 🌟 Key Features

- **📄 Dynamic PDF Ingestion**: Upload any PDF document (handles large documents like 150+ page textbooks seamlessly).
- **🧩 Enterprise Modular Architecture**: Decoupled codebase separated into `config.py`, `prompt_templates.py`, `rag_pipeline.py`, and `app.py`.
- **🚀 Modern LangChain LCEL**: Built using LangChain Expression Language (`RunnablePassthrough`, `PromptTemplate`, `ChatOpenAI`, `StrOutputParser`) instead of deprecated chains.
- **💬 Humanized & Grounded Responses**: Conversational, warm, and accurate answers generated strictly from retrieved context without inventing facts.
- **📚 Source Attribution**: Displays exact PDF filenames, page numbers (1-indexed), and text snippets for full traceability.
- **🛡️ Robust Error Handling & Stability**:
  - Filters out blank, scanned, or non-extractable pages to prevent empty chunk errors.
  - Native ChromaDB collection reset via `chromadb.PersistentClient` to prevent SQLite read-only / database locking errors (`code: 1032`).
  - Batch insertion to safely process large multi-page PDF documents.

---

## 🏗️ Architecture & Workflow

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
               │ Similarity Search (K) │ ◄─────── User Question
               └───────────┬───────────┘
                           │ Top-K Chunks
                           ▼
               ┌───────────────────────┐
               │ Humanized LCEL Prompt │
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

## 📁 Project Structure

```text
RAG/
│
├── config.py             # System configuration, paths, and OpenAI model parameters
├── prompt_templates.py   # Humanized prompt engineering templates
├── rag_pipeline.py       # Core RAG engine (Document loader, Chunking, ChromaDB, LCEL)
├── app.py                # Streamlit web application frontend
├── requirements.txt      # Project dependencies
├── .env                  # Environment variables (OpenAI API key)
├── .env.example          # Template for environment variables
└── .gitignore            # Git ignore rules
```

### Module Responsibilities

1. **`config.py`**: Manages environment variables, directory paths (`uploaded_pdfs/`, `chroma_db/`), model settings (`gpt-4o-mini`, `text-embedding-3-small`), and default chunking parameters.
2. **`prompt_templates.py`**: Contains prompt templates designed to generate articulate, warm, humanized, and well-formatted answers while enforcing context boundary rules.
3. **`rag_pipeline.py`**: Handles text extraction, empty page filtering, document chunking, batch vector creation, similarity retrieval, and LCEL chain execution.
4. **`app.py`**: Implements the clean Streamlit UI with file uploader, session state management, chat interface, and expandable source citations.

---

## ⚙️ Prerequisites & Setup

### 1. Prerequisites
- Python `3.10+`
- OpenAI API Key

### 2. Installation Steps

1. **Clone or navigate to the repository directory:**
   ```bash
   cd /Volumes/Personal/RAG
   ```

2. **Create and activate a Python virtual environment (optional but recommended):**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure your OpenAI API Key:**
   Create a `.env` file in the root directory (or copy from `.env.example`):
   ```bash
   cp .env.example .env
   ```
   Add your OpenAI API key to `.env`:
   ```env
   OPENAI_API_KEY=your_actual_openai_api_key_here
   ```

---

## 🚀 Running the Application

Launch the Streamlit server:

```bash
python3 -m streamlit run app.py
```

Once started, open your web browser at:
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
