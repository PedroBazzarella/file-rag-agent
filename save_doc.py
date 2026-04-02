from rag.embedding import chunk_n_store

# Loop de execução do salvamento dos documentos no banco de dados
def save_documents() -> None:
    print("Fazer upload de documentos para embedding.")
    while True:
        doc_path = input("Digite a URL do documento (ou apenas ENTER para ir ao chat): ")
        if not doc_path:
            break
        try:
            chunk_n_store(doc_path)
        except Exception as e:
            raise RuntimeError(f"Erro no salvamento do documento: '{doc_path}'") from e
        finally:
            print("Documento salvo!")

    print()