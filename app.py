"""Bare bones RAG chatbot that answers questions about the documents in DATA_DIR."""

import os
from pathlib import Path

import httpx
import streamlit as st
from dotenv import load_dotenv
from google.genai import errors as genai_errors
from llama_index.core import Settings, SimpleDirectoryReader, VectorStoreIndex
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.google_genai import GoogleGenAI

DATA_DIR = Path("data") / "handbook"
LLM_MODEL = "gemini-2.5-flash"
EMBED_MODEL = "BAAI/bge-small-en-v1.5"

load_dotenv()


def get_api_key():
    """Return the Gemini API key from .env, or stop the app if it is missing."""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        st.error(
            "GEMINI_API_KEY was not found. Add the line "
            "`GEMINI_API_KEY=your_key_here` to the .env file in your project "
            "folder, then restart the app."
        )
        st.stop()
    return api_key


def check_data_dir():
    """Stop the app unless DATA_DIR exists, is a folder, and has a visible file."""
    if not DATA_DIR.is_dir():
        st.error(
            f"Could not find the folder `{DATA_DIR}`. Create it inside your "
            "project folder and put the documents you want to chat with in it."
        )
        st.stop()

    # Ignore hidden files like .DS_Store, since SimpleDirectoryReader skips them too.
    visible_files = [
        f for f in DATA_DIR.iterdir() if f.is_file() and not f.name.startswith(".")
    ]
    if not visible_files:
        st.error(
            f"The folder `{DATA_DIR}` has no documents in it. Add at least one "
            "file (PDF, TXT, etc.) and restart the app."
        )
        st.stop()


@st.cache_resource
def get_query_engine(api_key):
    """Load the documents, build the vector index once, and return a query engine."""
    Settings.llm = GoogleGenAI(model=LLM_MODEL, api_key=api_key)
    Settings.embed_model = HuggingFaceEmbedding(model_name=EMBED_MODEL)
    documents = SimpleDirectoryReader(str(DATA_DIR)).load_data()
    index = VectorStoreIndex.from_documents(documents)
    return index.as_query_engine()


st.title("Bare Bones RAG Chatbot")

# Fail fast: check the setup before doing any expensive work.
api_key = get_api_key()
check_data_dir()

try:
    query_engine = get_query_engine(api_key)
except ValueError as e:
    st.error(f"Could not read the documents in `{DATA_DIR}`. Details: {e}")
    st.stop()
except OSError as e:
    st.error(
        "Could not load the embedding model or a document. Check your internet "
        f"connection and that your files open normally, then restart. Details: {e}"
    )
    st.stop()
except Exception as e:
    st.error(f"Something went wrong while building the index. Details: {e}")
    st.stop()

prompt = st.chat_input("Ask me anything...")
if prompt:
    st.write(f"User: {prompt}")
    with st.chat_message("assistant"):
        # Fallback: a failed question shows an error, but the app keeps running.
        try:
            with st.spinner("Searching..."):
                response = query_engine.query(prompt)
            st.write(f"Bot response: {response.response}")
        except genai_errors.APIError as e:
            st.error(
                f"Gemini returned an error ({e.code}). If it's a rate limit (429), "
                f"wait a minute and ask again. Details: {e.message}"
            )
        except (httpx.TransportError, ConnectionError, TimeoutError):
            st.error("Could not reach Gemini. Check your internet connection and ask again.")
        except Exception as e:
            st.error(f"Something went wrong answering that question. Details: {e}")