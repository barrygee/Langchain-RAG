from langchain.prompts import ChatPromptTemplate

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
