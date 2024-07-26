import os
from langchain_community.embeddings import OllamaEmbeddings
from langchain_postgres.vectorstores import PGVector

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
