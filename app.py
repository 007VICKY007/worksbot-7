import os
import shutil
from pathlib import Path
import streamlit as st

from config import UPLOAD_DIR, VECTOR_DB_DIR
from rag_pipeline import RAGPipeline

# Streamlit Page Setup
st.set_page_config(
    page_title="Conversational RAG PDF Assistant",
    layout="wide"
)

# Custom Styling
st.markdown("""
<style>
    .main .block-container { max-width: 900px; padding-top: 2rem; }
    .stButton button { border-radius: 6px; }
</style>
""", unsafe_allow_html=True)

# Session State Initialization
if "rag_pipeline" not in st.session_state:
    st.session_state.rag_pipeline = None

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "initialized" not in st.session_state:
    st.session_state.initialized = False

if "file_summary" not in st.session_state:
    st.session_state.file_summary = ""

# Sidebar UI
with st.sidebar:
    st.title("Document Upload")
    st.caption("Upload PDF documents to build vector index")

    # API key check
    active_api_key = os.getenv("OPENAI_API_KEY")
    if not active_api_key:
        st.warning("OpenAI API Key Required")
        active_api_key = st.text_input("Enter OpenAI API Key:", type="password")
        if active_api_key:
            os.environ["OPENAI_API_KEY"] = active_api_key

    uploaded_files = st.file_uploader(
        "Select PDF Document(s)",
        type=["pdf"],
        accept_multiple_files=True
    )

    if st.button("Process PDF & Build Pipeline", type="primary", use_container_width=True):
        if not uploaded_files:
            st.error("Please upload at least one PDF document.")
        elif not active_api_key:
            st.error("Please enter a valid OpenAI API Key.")
        else:
            with st.spinner("Extracting text, chunking & indexing vector embeddings..."):
                try:
                    # Clear session pipeline reference
                    st.session_state.rag_pipeline = None

                    # Clean upload directory safely
                    if UPLOAD_DIR.exists():
                        for f in UPLOAD_DIR.glob("*.pdf"):
                            try:
                                f.unlink()
                            except Exception:
                                pass
                    else:
                        UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

                    # Save newly uploaded PDF files
                    file_names = []
                    for file in uploaded_files:
                        file_path = UPLOAD_DIR / file.name
                        with open(file_path, "wb") as f:
                            f.write(file.getbuffer())
                        file_names.append(file.name)

                    # Instantiate & Initialize RAG Pipeline
                    pipeline = RAGPipeline(
                        pdf_path=UPLOAD_DIR,
                        persist_directory=VECTOR_DB_DIR,
                        api_key=active_api_key
                    )
                    pipeline.initialize()

                    st.session_state.rag_pipeline = pipeline
                    st.session_state.initialized = True
                    st.session_state.chat_history = []
                    st.session_state.file_summary = f"{len(file_names)} file(s): " + ", ".join(file_names)

                    st.success("RAG Pipeline ready.")
                    st.rerun()

                except Exception as e:
                    st.error(f"Error processing PDF: {str(e)}")

    st.divider()

    if st.session_state.initialized:
        st.caption("Active Document:")
        st.info(st.session_state.file_summary)

        if st.button("Upload New Document", use_container_width=True):
            st.session_state.rag_pipeline = None
            st.session_state.initialized = False
            st.session_state.chat_history = []
            st.session_state.file_summary = ""
            st.rerun()

# Main Area UI
st.title("RAG PDF Assistant")

if not st.session_state.initialized:
    st.info("Upload your PDF in the sidebar and click Process PDF & Build Pipeline to start chatting.")
else:
    # Render Chat History
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

            if message["role"] == "assistant" and message.get("sources"):
                with st.expander(f"View Retrieved Sources ({len(message['sources'])})"):
                    for idx, src in enumerate(message["sources"], 1):
                        st.markdown(f"**Source {idx}:** `{src['source']}` (Page {src['page']})")
                        st.markdown(f"```text\n{src['content']}\n```")

    # Chat Input Box
    user_input = st.chat_input("Ask any question in the PDF document...")

    if user_input:
        # Display User Message
        with st.chat_message("user"):
            st.markdown(user_input)

        # Process Query with Conversation History for History-Aware Retrieval & Answers
        with st.chat_message("assistant"):
            with st.spinner("Searching document context & generating response..."):
                res = st.session_state.rag_pipeline.query(
                    question=user_input,
                    chat_history=st.session_state.chat_history
                )
                answer = res["answer"]
                sources = res["source_documents"]

                st.markdown(answer)

                formatted_sources = []
                is_not_available = (
                    "could not find information" in answer.lower()
                    or "not present" in answer.lower()
                    or "not available" in answer.lower()
                )

                if sources and not is_not_available:
                    with st.expander(f"View Retrieved Sources ({len(sources)})"):
                        for idx, doc in enumerate(sources, 1):
                            src_name = Path(doc.metadata.get("source", "PDF")).name
                            page_num = doc.metadata.get("page", 0) + 1
                            snippet = doc.page_content

                            st.markdown(f"**Source {idx}:** `{src_name}` (Page {page_num})")
                            st.markdown(f"```text\n{snippet}\n```")

                            formatted_sources.append({
                                "source": src_name,
                                "page": page_num,
                                "content": snippet
                            })

                # Append user message and assistant answer to session history
                st.session_state.chat_history.append({"role": "user", "content": user_input})
                st.session_state.chat_history.append({
                    "role": "assistant",
                    "content": answer,
                    "sources": formatted_sources
                })
