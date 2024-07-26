def retrieve_relevant_documents(vectorstore, question):
    retriever = vectorstore.as_retriever(
        search_type="similarity_score_threshold",
        search_kwargs={'k': 5, 'score_threshold': 0.1}
    )

    relevant_docs = retriever.invoke(question)
    return relevant_docs
