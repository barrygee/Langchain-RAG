import uuid
from env_loader import load_environment_variables
from callback_handler import initialize_callback_handler
from document_handler import load_documents, split_documents
from vector_embeddings import create_and_store_embeddings
from document_retrieval import retrieve_relevant_documents
from model_initialization import initialize_model
from prompt_template import create_prompt_template
from chain_creation import create_chain

def main(question="What science is being conducted during the mission?"):
    session_id = str(uuid.uuid4())
    model_name, host_service_url, secret_key, public_key, langfuse_host, langfuse_tags_environment, langfuse_tags_application_version = load_environment_variables()
    langfuse_handler = initialize_callback_handler(secret_key, public_key, langfuse_host, langfuse_tags_environment, langfuse_tags_application_version, session_id)

    documents = load_documents()
    docs = split_documents(documents)

    vectorstore = create_and_store_embeddings(docs)
    relevant_docs = retrieve_relevant_documents(vectorstore, question)

    model = initialize_model(model_name, host_service_url)
    prompt_template = create_prompt_template()

    config = {"callbacks": [langfuse_handler]}
    chain = create_chain(prompt_template, model)
    result = chain.invoke({"context": relevant_docs, "question": question}, config=config)

    print('ANSWER: ', result)

if __name__ == "__main__":
    main()
