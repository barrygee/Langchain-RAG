import os
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

def load_documents():
    current_directory = os.path.dirname(os.path.abspath(__file__))
    docs_directory_path = os.path.join(current_directory, "./docs")
    pdfs = [p for p in os.listdir(docs_directory_path) if p.endswith(".pdf")]
    documents = []

    for pdf in pdfs:
        file_path = os.path.join(docs_directory_path, pdf)
        loader = PyPDFLoader(file_path)
        pdf_docs = loader.load()
        documents.extend(pdf_docs)
        for doc in pdf_docs:
            documents.append(doc)

    return documents

def split_documents(documents):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=50)
    docs = text_splitter.split_documents(documents)
    return docs
