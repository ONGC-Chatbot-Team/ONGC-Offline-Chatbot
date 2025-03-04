import streamlit as st
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.embeddings import HuggingFaceInstructEmbeddings
from langchain_community.vectorstores import FAISS
from sentence_transformers import SentenceTransformer
import numpy as np
import asyncio
import sys

if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

asyncio.set_event_loop(asyncio.new_event_loop())  # Force reset


def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            extracted_text = page.extract_text()
            if extracted_text:  # Avoid appending None values
                text += extracted_text + "\n"
    return text

def get_text_chunks(text):
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=500,
        chunk_overlap=100,
        length_function=len
    )
    chunks = text_splitter.split_text(text)
    return chunks

def get_vectorstore(text_chunks):
    print("Generating embeddings...") 
    model = SentenceTransformer("all-MiniLM-L6-v2")
    embeddings = model.encode(text_chunks, convert_to_numpy=True)

    # Store in FAISS for similarity search
    faiss_store = FAISS.from_embeddings(embeddings, text_chunks)
    print("Embeddings stored successfully in FAISS!")
    
    return faiss_store

def main():
    load_dotenv()
    st.set_page_config(
        page_title="Oil and Natural Gas Corporation Limited Epinet Manual Chatbot",
        page_icon="🔍",
        layout="centered",
        initial_sidebar_state="auto"
    )

    st.header("Oil and Natural Gas Corporation Limited Epinet Manual Chatbot")
    st.text("This chatbot is designed to help you with your queries related to ONGC's Epinet Manual.")

    query = st.text_input("Enter your queries related to the manual here:")
    
    with st.sidebar:
        st.subheader("Upload the PDF file of the Manual here:")
        pdf_docs = st.file_uploader("Upload PDF and click Add", accept_multiple_files=True, type=["pdf"])

        if st.button("Add"):
            with st.spinner("Uploading..."):
                # Extract text from PDFs
                raw_text = get_pdf_text(pdf_docs)

                # Get the text chunks
                text_chunks = get_text_chunks(raw_text)

                # Create vector store
                vectorstore = get_vectorstore(text_chunks)

                st.success("PDF uploaded and processed successfully!")

if __name__ == '__main__':
    main()
