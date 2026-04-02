from config import OLLAMA_CHAT_MODEL, OLLAMA_EMBEDDING_MODEL, OLLAMA_BASE_URL, WEAVIATE_GRPC_PORT, WEAVIATE_HOST, WEAVIATE_HTTP_PORT

from agent.core import get_chat_model, get_embedding_model, get_retriever
from agent.chain import get_chain
from save_doc import save_documents

import weaviate
import httpx
import json

from langchain_core.runnables import RunnableSerializable

# Requisisão para o ollama para baixar os modelos
def pull_ollama_models() -> None:
    models = [OLLAMA_CHAT_MODEL, OLLAMA_EMBEDDING_MODEL]
    
    with httpx.Client() as client:
        response = client.get(f"{OLLAMA_BASE_URL}/api/tags")
        already_pulled = {m["name"] for m in response.json().get("models", [])}

        for model in models:
            # Verifica se já foi baixado
            if model in already_pulled:
                print(f"Modelo '{model}' já disponível.")
                continue
            
            # Baixa se necessário
            print(f"Fazendo pull do modelo '{model}'...")
            with client.stream("POST", f"{OLLAMA_BASE_URL}/api/pull", json={"name": model}) as r:
                # Resposta visual de progresso do download
                for line in r.iter_lines():
                    data = json.loads(line)
                    total = data.get("total")
                    completed = data.get("completed")
                    status = data.get("status", "")

                    if total and completed:
                        percent = (completed / total) * 100
                        print(f"\r{status}: {percent:.1f}%", end="", flush=True)
                    else:
                        print(f"\rr{status}", end="", flush=True)
            
            print()

# Loop do chat para terminal
def chat_loop(chain: RunnableSerializable) -> None:
    pull_ollama_models()

    print("\n\n-- Assistente Governanca de Dados --\nDigite 'sair' para encerrar.\n")

    # Chama loop de fazer salvamento e embedding de documentos via URLs
    save_documents()

    while True:
        prompt = input("Você: ")
        
        if not prompt:
            continue

        if prompt.lower() == "sair":
            print("Encerrando a conversa.")
            break

        print("Assistente: ", end="", flush=True)

        # Chama a chain com streaming de resposta
        try:
            for chunk in chain.stream(prompt):
                print(chunk, end="", flush=True)
            print()
        except Exception as e:
            raise RuntimeError(f"Erro ao processar a solicitação: {e}")

def main() -> None:
    print("Iniciando o assistente...")

    # Cria conexão com o weaviate
    try:
        weaviate_client = weaviate.connect_to_custom(
            http_host=WEAVIATE_HOST,
            http_port=WEAVIATE_HTTP_PORT,
            http_secure=False,
            grpc_host=WEAVIATE_HOST,
            grpc_port=WEAVIATE_GRPC_PORT,
            grpc_secure=False,
        )
    except Exception as e:
        raise RuntimeError(f"Erro conectando ao Weaviate: {e}")
    
    try:
        # Cria as conexões com o ollama
        chat_model = get_chat_model()
        embedding_model = get_embedding_model()

        # Cria o retriever
        retriever = get_retriever(weaviate_client, embedding_model)

        # Define a chain
        chain = get_chain(retriever, chat_model)

        chat_loop(chain)
    except Exception as e:
        raise RuntimeError(f"Erro ao inicializar o chat: {e}")
    finally:
        # Fecha conexão com o weaviate
        weaviate_client.close()

        # Fecha conexões com o ollama
        if hasattr(embedding_model, '_client') and hasattr(embedding_model._client, '_client') and embedding_model._client:
            embedding_model._client._client.close()
        if hasattr(chat_model, '_client') and hasattr(chat_model._client, '_client'):
            chat_model._client._client.close()

if __name__ == "__main__":
    main()