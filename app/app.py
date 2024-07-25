from dotenv import load_dotenv
import os

from langchain_community.llms import Ollama
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import OllamaEmbeddings
from langchain_postgres.vectorstores import PGVector
from langchain.prompts import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser
from langchain.prompts import ChatPromptTemplate
from langfuse.callback import CallbackHandler


# Environment variables

def load_environment_variables():
  load_dotenv()
  
  model = os.getenv("MODEL_NAME")
  host_service_url = os.getenv('HOST_SERVICE_URL')
  secret_key=os.getenv("LANGFUSE_SECRET_KEY")
  public_key=os.getenv("LANGFUSE_PUBLIC_KEY")
  langfuse_host=os.getenv("LANGFUSE_HOST")
  langfuse_tags_environment=os.getenv("LANGFUSE_TAGS_ENVIRONMENT")
  langfuse_tags_application_version=os.getenv("LANGFUSE_TAGS_APPLICATION_VERSION")

  return model, host_service_url, secret_key, public_key, langfuse_host, langfuse_tags_environment, langfuse_tags_application_version



# Initialize CallbackHandler

def initialize_callback_handler(secret_key, public_key, langfuse_host, langfuse_tags_environment, langfuse_tags_application_version):
    langfuse_handler = CallbackHandler(
      secret_key=secret_key,
      public_key=public_key,
      host=f"http://{langfuse_host}:3000",
      tags=[
        langfuse_tags_environment,
        langfuse_tags_application_version
      ]
    )
    return langfuse_handler



# Load and split documents from the /app/docs directory

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



# Create vector embeddings from the chunked documents and save into PGVector database

def create_and_store_embeddings(docs):
  embeddings = OllamaEmbeddings(model='nomic-embed-text', base_url=f"http://{os.getenv('HOST_SERVICE_URL')}")

  connection_string = f"postgresql+psycopg2://{os.getenv('POSTGRES_USERNAME')}:{os.getenv('POSTGRES_PASSWORD')}@{os.getenv('POSTGRES_HOST')}:{os.getenv('POSTGRES_PORT')}/{os.getenv('POSTGRES_DB')}"
  collection_name = os.getenv('PGVECTOR_COLLECTION_NAME')

  vectorstore = PGVector.from_documents(
      embedding=embeddings,
      documents=docs,
      connection=connection_string,
      collection_name=collection_name,
      use_jsonb=True,
      async_mode=False,
  )

  return vectorstore



# Document retrieval

def retrieve_relevant_documents(vectorstore, question):
  retriever = vectorstore.as_retriever(
      search_type="similarity_score_threshold",
      search_kwargs={'k': 5, 'score_threshold': 0.1}
  )

  relevant_docs = retriever.invoke(question)
  return relevant_docs



# LLM 

def initialize_model(model_name, host_service_url):
  model = Ollama(
      model=model_name,
      base_url=f"http://{host_service_url}",
      temperature=2
  )
  return model



# Prompt template

def create_prompt_template():
  template = """Answer the question based on the following context: {context}
  If you are unable to find the answer within the context, please respond with 'I don't know'.

  Question: {question}
  """
  prompt_template = ChatPromptTemplate.from_messages(
      [
          ("system", template),
          ("human", "{question}")
      ]
  )
  return prompt_template



# Langchain chain

def create_chain(prompt_template, model):
  chain = prompt_template | model | StrOutputParser()
  return chain



# Initiate the application

def main(question = "What science is being conducted during the mission?"):
  model_name, host_service_url, secret_key, public_key, langfuse_host, langfuse_tags_environment, langfuse_tags_application_version  = load_environment_variables()
  langfuse_handler = initialize_callback_handler(secret_key, public_key, langfuse_host, langfuse_tags_environment, langfuse_tags_application_version)

  documents = load_documents()
  docs = split_documents(documents)

  vectorstore = create_and_store_embeddings(docs)
  relevant_docs = retrieve_relevant_documents(vectorstore, question)

  model = initialize_model(model_name, host_service_url)
  prompt_template = create_prompt_template()
  
  config = {"callbacks": [langfuse_handler]}
  chain = create_chain(prompt_template, model) 
  result = chain.invoke({"context": relevant_docs, "question": question}, config=config)
  
  print(result)

if __name__ == "__main__":
    main()
