import os

# Ollama
OLLAMA_CHAT_MODEL = os.getenv("OLLAMA_CHAT_MODEL") or "qwen3:4b-instruct-2507-q4_K_M"
OLLAMA_EMBEDDING_MODEL = os.getenv("OLLAMA_EMBEDDING_MODEL") or "embeddinggemma"

OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL") or "http://ollama:11434"

# Chunking
MIN_CHUNKING_SIZE = int(os.getenv("MIN_CHUNKING_SIZE") or "50")

# Weaviate
INDEX_NAME = os.getenv("INDEX_NAME") or "Docs"

WEAVIATE_HOST = os.getenv("WEAVIATE_HOST") or "weaviate"
WEAVIATE_HTTP_PORT = int(os.getenv("WEAVIATE_HTTP_PORT") or "8080")
WEAVIATE_GRPC_PORT = int(os.getenv("WEAVIATE_GRPC_PORT") or "50051")