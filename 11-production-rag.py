"""
RAG Chatbot for the Babson Handbook
I have subbed Groq for Gemini API.
However these Gemini models supposedly work:
gemini-3.8-flash, gemini-3-flash 
I didn't test because I wanted to play with Groq 
"""
import os
import streamlit as st
from dotenv import load_dotenv
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings
from llama_index.core.base.response.schema import Response  # Fix type annotation inspection
from llama_index.llms.groq import Groq
from llama_index.embeddings.huggingface import HuggingFaceEmbedding

# noinspection SpellCheckingInspection
# --- CONFIGURATION & ENVIRONMENT SETUP ---
load_dotenv()
DATA_DIR = "data/handbook"


# --- GLOBAL ONCE-PER-SESSION RESOURCE CACHE ---
@st.cache_resource
def initialize_global_settings():
    """
    Caches the creation of the LLM and Embedding models.
    This stops local laptops from rebuilding the model architectures on every single rerun.
    """
    llm = Groq(model="openai/gpt-oss-20b")
    # Caching this prevents severe local CPU slowdowns during prompt translation
    embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")
    return llm, embed_model


# Run initialization immediately to seed the global configuration state
Settings.llm, Settings.embed_model = initialize_global_settings()


@st.cache_resource
def setup_rag_engine():
    """
    Performs the essential Loading and Indexing steps only once.
    """
    if not os.getenv("GROQ_API_KEY"):
        st.error("❌ GROQ_API_KEY not found in .env file.")
        st.stop()

    st.info("📚 Loading documents and creating index...")

    # 1. LOAD: Load documents from the target directory
    documents = SimpleDirectoryReader(DATA_DIR).load_data()

    # 2. INDEX: Create a searchable vector index from the documents
    # Passing documents list matches strict index layout parameters
    index = VectorStoreIndex.from_documents(documents=documents)

    st.success("✅ RAG Indexing Complete.")

    # 3. QUERY: Create and return the final query engine instance
    return index.as_query_engine()


# noinspection SpellCheckingInspection
# --- STREAMLIT ENGINE INITIALIZATION ---
st.set_page_config(page_title="Babson Handbook RAG Chatbot", layout="centered")
st.title("👨‍🎓 Babson Handbook RAG Chatbot")
st.markdown("Ask questions grounded in the student handbook.")

# Initialize the resource-intensive RAG engine via cache
query_engine = setup_rag_engine()

# Initialize conversational state tracking
if "messages" not in st.session_state:
    st.session_state.messages = []

# Render chronological chat history on app redraw
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- LIVE INTERACTION FLOW ---
# Accept user input (Returns a ChatInputValue object because accept_file=True)
user_input_obj = st.chat_input("Ask a question about the handbook...", accept_file=True)

if user_input_obj:
    # Extract the raw text string directly from the object container
    clean_text_query = user_input_obj.text

    # Append the clean string to memory state
    st.session_state.messages.append({"role": "user", "content": clean_text_query})

    # Display the query immediately to the user interface
    with st.chat_message("user"):
        st.markdown(clean_text_query)

    # Execute backend retrieval and model generation
    with st.chat_message("assistant"):
        with st.spinner("Searching and synthesizing..."):
            # Pass the extracted string into LlamaIndex seamlessly
            response = query_engine.query(clean_text_query)
            bot_response = response.response

        st.markdown(bot_response)

    # Append the synthesized response to tracking state
    st.session_state.messages.append({"role": "assistant", "content": bot_response})
