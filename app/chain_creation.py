from langchain.schema.output_parser import StrOutputParser

def create_chain(prompt_template, model):
    chain = prompt_template | model | StrOutputParser()
    return chain
