import os
from dotenv import load_dotenv

def load_environment_variables():
    load_dotenv()

    model = os.getenv("MODEL_NAME")
    host_service_url = os.getenv('HOST_SERVICE_URL')
    secret_key = os.getenv("LANGFUSE_SECRET_KEY")
    public_key = os.getenv("LANGFUSE_PUBLIC_KEY")
    langfuse_host = os.getenv("LANGFUSE_HOST")
    langfuse_tags_environment = os.getenv("LANGFUSE_TAGS_ENVIRONMENT")
    langfuse_tags_application_version = os.getenv("LANGFUSE_TAGS_APPLICATION_VERSION")

    return model, host_service_url, secret_key, public_key, langfuse_host, langfuse_tags_environment, langfuse_tags_application_version
