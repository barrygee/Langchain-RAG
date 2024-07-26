from langfuse.callback import CallbackHandler

def initialize_callback_handler(secret_key, public_key, langfuse_host, langfuse_tags_environment, langfuse_tags_application_version, session_id):
    langfuse_handler = CallbackHandler(
        secret_key=secret_key,
        public_key=public_key,
        host=f"http://{langfuse_host}:3000",
        tags=[
            langfuse_tags_environment,
            langfuse_tags_application_version
        ],
        session_id=session_id
    )
    return langfuse_handler
