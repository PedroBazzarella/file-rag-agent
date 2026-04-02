from config import WEAVIATE_GRPC_PORT, WEAVIATE_HOST, WEAVIATE_HTTP_PORT, INDEX_NAME

from agent.core import get_embedding_model
from rag.chunking import chunk_document

import weaviate

from langchain_weaviate import WeaviateVectorStore
from langchain_core.documents import Document

# Chama o chunking, passa pelo embedder e salva no weaviate
def chunk_n_store(doc_path: str):
    try:
        text_from_document = chunk_document(doc_path)
        documents = [Document(page_content=text) for text in text_from_document]

        if not documents:
            raise ValueError(f"Retorno do chunking do documento esta vazio: '{doc_path}'")
        
        print("Iniciando embedding do documento...")

        embedding_model = get_embedding_model()

        client = None
        client = weaviate.connect_to_custom(
            http_host=WEAVIATE_HOST,
            http_port=WEAVIATE_HTTP_PORT,
            http_secure=False,
            grpc_host=WEAVIATE_HOST,
            grpc_port=WEAVIATE_GRPC_PORT,
            grpc_secure=False,
        )

        WeaviateVectorStore.from_documents(
            documents=documents,
            embedding=embedding_model,
            client=client,
            index_name=INDEX_NAME,
        )

        print("Embedding concluido.")
    except Exception as e:
        raise RuntimeError(f"Erro no embedding do documento: '{doc_path}'") from e
    
    finally:
        if client is not None:
            client.close()