import streamlit as st
from dotenv import load_dotenv



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


                #get the text chunks


                #create vector store

if __name__ == '__main__':
    main()