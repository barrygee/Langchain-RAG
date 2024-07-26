from langchain_community.llms import Ollama

def initialize_model(model_name, host_service_url):
    model = Ollama(
        model=model_name,
        base_url=f"http://{host_service_url}",
        temperature=2
    )
    return model
