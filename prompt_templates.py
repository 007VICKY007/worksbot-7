from langchain_core.prompts import PromptTemplate

# Prompt Template 1: Standalone Question Reformulation using Chat History
REFORMULATE_QUESTION_TEMPLATE = """Given a chat history and the latest user question which might reference context in the chat history, formulate a standalone question which can be understood without the chat history. Do NOT answer the question, just reformulate it if needed and otherwise return it as is.

Chat History:
{chat_history}

Latest Question: {question}

Standalone Question:"""

# Prompt Template 2: Conversational Humanized RAG Prompt Template
CONVERSATIONAL_RAG_TEMPLATE = """You are a helpful, articulate, and intelligent AI assistant answering questions based strictly on the provided document context and prior conversation history.

Instructions:
1. Provide a warm, clear, professional, and well-structured response using natural conversational language.
2. Use the Chat History to understand references (such as pronouns, follow-up requests, or previous topics).
3. Rely strictly on the information provided in the Context below. Do not invent or assume details that are not present in the document.
4. If the answer cannot be found in the context, state politely and naturally that the information is not present in the uploaded document.
5. Keep your formatting clean, professional, and easy to read (using bullet points when explaining complex steps).

Chat History:
{chat_history}

Context:
{context}

Question:
{question}

Answer:"""


def get_reformulate_prompt() -> PromptTemplate:
    """Return prompt template for question reformulation."""
    return PromptTemplate(
        template=REFORMULATE_QUESTION_TEMPLATE,
        input_variables=["chat_history", "question"]
    )


def get_conversational_rag_prompt() -> PromptTemplate:
    """Return conversational RAG prompt template."""
    return PromptTemplate(
        template=CONVERSATIONAL_RAG_TEMPLATE,
        input_variables=["chat_history", "context", "question"]
    )
