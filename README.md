# Langchain Retrieval Augmented Generation (RAG) application

- This application includes a containerised Langchain RAG application.
- Vector embeddings are stored in a locally running containerised PGVector database.
- LLM inputs and outputs, traces and prompts are monitored in a locally running containerised Langfuse installation.
- The application uses locally running LLMs made available via Ollama.


## Setup

### Ollama

Download and install Ollama

https://ollama.com


Download the required embedding model
```
ollama pull nomic-embed-text
```

Download and run the required LLM
```
ollama run phi3:mini
```
This should be the same model defined in the .env file 'MODEL_NAME'


### Docker

Next, run the application, vector database and Langfuse:

In the root directory run 
```
docker-compose up --build
```


## Langfuse

Once the Langfuse-server container is up and running;

If this is the first time you have setup the application:
- visit http://localhost:3000 in your browser
- Create a new account
- Click the 'New Project' button
- Name the project 'coreai-techspike-evaluations'
- Click 'Settings' in the left hand panel 
- Click 'Create new API keys'
- Copy the secret key and paste it into your .env file 'LANGFUSE_SECRET_KEY'
- Copy the public key and paste it into your .env file 'LANGFUSE_PUBLIC_KEY'
- Run ```docker compose down```
- Run ```docker compose up --build```



## PGVector

Reference: 
https://api.python.langchain.com/en/latest/vectorstores/langchain_postgres.vectorstores.PGVector.html#langchain_postgres.vectorstores.PGVector



## Python3 Environment - For code hinting

Create a new Python3 virtual environment
```
python3 -m venv venv
```

Activate the new Python3 virtual environment
```
source venv/bin/activate
```

Install the required dependencies into the new Python3 virtual environment
```
pip install -r requirements.txt
```