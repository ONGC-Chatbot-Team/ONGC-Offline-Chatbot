import streamlit as st
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter




def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        pdf_reader =  PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text


def get_text_chunks(text):
    text_splitter = CharacterTextSplitter(seperator = "\n", chunk_size = 1000, chunk_overlap =200,length_function = len)
    chunks = text_splitter.split_text(text)
    return chunks



def main():
    load_dotenv()
    st.set_page_config(page_title = "Oil and Natural Gas Corporation Limited Epinet Manual Chatbot", page_icon = "🔍", layout = "centered", initial_sidebar_state = "auto")

    st.header("Oil and Natural Gas Corporation Limited Epinet Manual Chatbot")
    st.text("This chatbot is designed to help you with your queries related to ONGC's Epinet Manual.")

    st.text_input("Enter your queries related to the manual here:")
    
    with st.sidebar:
        st.subheader("Upload the PDF file of the Manual here:")
        pdf_docs = st.file_uploader("Upload PDF and click Add", accept_multiple_files = True)

        if st.button("Add"):
            with st.spinner("Uploading..."):
                #get the pdf text
                raw_text = get_pdf_text(pdf_docs)

                #get the text chunks
                text_chunks = get_text_chunks(raw_text)
                st.write(text_chunks)


                #create vector store

if __name__ == '__main__':
    main()