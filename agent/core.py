from config import OLLAMA_CHAT_MODEL, OLLAMA_EMBEDDING_MODEL, OLLAMA_BASE_URL, INDEX_NAME

import weaviate
from langchain_ollama import ChatOllama, OllamaEmbeddings
from langchain_weaviate.vectorstores import WeaviateVectorStore
from langchain_core.vectorstores import VectorStoreRetriever

# Factories para conexões com ollama e retriever do weaviate

def get_chat_model() -> ChatOllama:
    llm = ChatOllama(
        model=OLLAMA_CHAT_MODEL,
        temperature=0.1,
        base_url=OLLAMA_BASE_URL,
    )
    return llm

def get_embedding_model() -> OllamaEmbeddings:
    embedding = OllamaEmbeddings(
        model=OLLAMA_EMBEDDING_MODEL,
        base_url=OLLAMA_BASE_URL,
    )
    return embedding

def get_retriever(client: weaviate.WeaviateClient, embedding: OllamaEmbeddings) -> VectorStoreRetriever:
    vector_store = WeaviateVectorStore(
        embedding=embedding,
        client=client,
        index_name=INDEX_NAME,
        text_key="text"
    )
    return vector_store.as_retriever()