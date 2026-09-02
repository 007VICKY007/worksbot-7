# Your Intelligent PDF Assistant

Ever wished you had a smart chatbot that actually *understands* your PDFs? Here's the thing: most chatbots just guess. This one? **It reads your documents first, then answers your questions.**

This is a **Retrieval-Augmented Generation (RAG)** PDF Chatbot built with Python and Streamlit. It's like having a personal research assistant who's read all your PDFs and remembers everything.

---

## What Can You Actually Do With This?

✓ **Upload ANY PDF** — Textbooks, research papers, contracts, manuals... doesn't matter.  
✓ **Ask Follow-Up Questions** — Say "what are the main points?" then follow up with "can you explain #2?"  
✓ **Get Exact Sources** — Every answer tells you *exactly* which PDF page it came from.  
✓ **Have Real Conversations** — The chatbot remembers what you asked before, so context actually sticks.  
✓ **No Guessing Games** — Answers are **always** grounded in your actual document content.

---

## How Does This Magic Work?

Think of it like this:

1. **You upload a PDF** → The app tears it apart into digestible chunks
2. **It converts to brain language** → Each chunk becomes a mathematical representation (embedding)
3. **Stores in a smart library** → ChromaDB indexes everything for lightning-fast retrieval
4. **You ask a question** → The chatbot finds the *most relevant* sections from your PDF
5. **It writes an answer** → Using OpenAI's GPT, it crafts a warm, human response based on what it found
6. **You see sources** → Exact filenames, page numbers, and the text snippets it used

**The Secret Sauce?** The chatbot understands conversational context. Ask "tell me more" and it knows you mean the previous topic—no re-explaining needed.

```
Your PDF  →  Extract & Chunk  →  Embed Text  →  Store in ChromaDB
                                                      |
                                             Your Question
                                                      |
                                        Find Relevant Sections
                                                      |
                                           Feed to GPT Model
                                                      |
                                        Conversational Answer
                                           + Source Citations
```

---

## What's Under the Hood?

- **LangChain LCEL** — Modern, clean, composable pipeline (no legacy spaghetti)
- **OpenAI Embeddings** — Smart text-to-vector conversion (text-embedding-3-small)
- **ChromaDB** — Blazing-fast vector database that remembers everything
- **Streamlit** — Beautiful web interface (no frontend headaches)
- **History-Aware** — Reformulates follow-up questions using full conversation context

---

## Project Organization

```
RAG/
├── config.py              # All your settings live here
├── prompt_templates.py    # How the chatbot talks to the LLM
├── rag_pipeline.py        # The brain of the operation
├── app.py                 # The pretty UI you interact with
├── requirements.txt       # Package list
├── .env                   # Your API keys (keep this secret!)
├── .env.example           # Template to get you started
└── .gitignore             # Don't commit your secrets
```

---

## Getting Started (5 Minutes)

### Step 1: Make Sure You Have Python
You'll need Python 3.10 or newer. [Don't have it?](https://www.python.org/downloads/)

### Step 2: Get an OpenAI API Key
Head to [platform.openai.com](https://platform.openai.com), sign up, and grab your API key. This is what powers the smart answers.

### Step 3: Clone & Install

```bash
# Navigate to your project folder
cd /path/to/your/RAG

# Install everything you need
pip install -r requirements.txt
```

### Step 4: Add Your API Key
Create a `.env` file in the project root:

```env
OPENAI_API_KEY=your_actual_key_here
```

(Check `.env.example` if you get stuck)

---

## Time to Run It

```bash
streamlit run app.py
```

That's it! Your browser should open to:  
**http://localhost:8501**

If it doesn't, just copy-paste that URL into your browser.

---

## How to Actually Use This

### First Time Setup
1. **Open the sidebar** (hamburger menu on the left)
2. **Click "Upload Document"** and pick one or more PDFs
3. **Smash the Process Button** — "Process PDF & Build Pipeline"
4. **Wait a sec** — It's working hard extracting, chunking, and embedding your documents

### Asking Questions
1. **Type anything** in the chat box at the bottom
2. **Hit enter** and watch it think
3. **Get your answer** with exact citations

### Follow-Up Questions
- "What's the main point?" → "Can you elaborate?" → "How does that relate to X?"
- The chatbot *remembers* the conversation, so you don't have to repeat context

### Check Your Sources
- Each answer has a **View Retrieved Sources** section
- Click it to see the exact pages and text snippets used
- Perfect for verifying facts or diving deeper

### Start Fresh
- Click **Upload New Document** anytime to wipe everything and start over

---

## What Makes This Robust?

- **Handles Messy PDFs** → Automatically filters out blank pages or weird formatting
- **No Database Crashes** → Uses PersistentClient to avoid SQLite locking headaches
- **Batch Processing** → Inserts embeddings efficiently, never gets overwhelmed
- **Error Handling** → If something breaks, you get a helpful message (not a cryptic crash)

---

## The Architecture (For the Curious)

```
+-----------------+
|   Your PDFs     |
+--------+--------+
         | PyPDFLoader
         v
+-----------------+
| Extract Text    |
+--------+--------+
         | RecursiveCharacterSplitter
         v
+-----------------+
| Chunk It Up     | <- Smart splitting, preserves meaning
+--------+--------+
         | OpenAI API
         v
+-----------------+
|Create Embeddings| <- Convert text to vectors
+--------+--------+
         | ChromaDB
         v
+-----------------+
|Vector Database  | <- Ready for lightning-fast search
+--------+--------+
         | Your Question
         |
         +---> Find most relevant chunks
         |
         +---> Build Full Prompt <- Add context & history
         |
         v
      GPT-4o-mini <- Generate smart answer
         |
         v
    Return to User <- Answer + citations
```

---

## Pro Tips

### Uploading Multiple PDFs?
Go ahead! The system chunks and embeds them all together, so you can ask questions across multiple documents.

### API Costs?
- **Embeddings** are cheap ($0.02 per 1M tokens)
- **Chat** varies based on your questions
- Start with a free trial to test things out

### Slow Responses?
- First time embedding is slower (it's doing real work)
- Subsequent questions are instant (ChromaDB caches everything)

### Quality Answers?
- Better PDFs = better answers (obviously)
- Specific questions beat vague ones
- Context matters—ask follow-ups naturally

---

## What You Need to Install

All in `requirements.txt`, but here's what's doing the heavy lifting:

- `langchain` — Pipeline orchestration
- `streamlit` — Beautiful UI
- `chromadb` — Vector storage
- `openai` — Smart LLM & embeddings
- `pypdf` — Reading PDFs like a boss

Just run `pip install -r requirements.txt` and you're golden.

---

## Something Broke?

**API Key not working?**  
Double-check your `.env` file and make sure your OpenAI account has billing enabled.

**PDFs not uploading?**  
Try a smaller file first, ensure it's actually a PDF (not scanned image).

**Slow responses?**  
First embed takes time, but questions 2+ are instant.

**Need help?**  
Check the `.env.example` file and make sure your setup matches.

---

**Happy document chatting!**  
Your PDFs just got a lot smarter.
