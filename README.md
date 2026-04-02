# File RAG Agent

## Visão Geral

O **File RAG Agent** é um assistente inteligente baseado em Retrieval-Augmented Generation (RAG) projetado para alunos de faculdade. Ele permite o upload de documentos via URLs, processa e armazena embeddings vetoriais usando Docling e Weaviate, e responde perguntas com base no contexto recuperado dos documentos. O sistema utiliza modelos de linguagem hospedados no Ollama para geração de respostas e incorporação de texto.

### Funcionalidades Principais
- **Upload de Documentos**: Suporte para URLs de documentos (PDF, DOCX, etc.) que são processados, divididos em chunks e armazenados como embeddings.
- **Chat Interativo**: Interface de terminal para perguntas e respostas em tempo real.
- **Integração com Ollama**: Utiliza modelos de chat e embedding locais via Ollama.
- **Banco Vetorial Weaviate**: Armazenamento e recuperação eficiente de vetores para RAG.
- **Containerização**: Execução simplificada com Docker Compose.

## Instalação

### Pré-requisitos
- Docker e Docker Compose instalados no sistema. (Se preferir pode rodar localmente)
- Para rodar os modelos da configuração padrão em memória é recomendado ao menos 8GB de RAM disponível.

### Passos de Instalação (Docker)
1. **Clone o repositório**:
    ```bash
    git clone https://github.com/PedroBazzarella/file-rag-agent.git
    cd file-rag-agent
    ```

2. **Execute com Docker Compose**:
    ```bash
    docker compose up --build weaviate ollama
    ```
    Isso iniciará os serviços:
    - **Weaviate**: Banco de dados vetorial (porta 8080).
    - **Ollama**: Servidor de modelos de IA (porta 11434).

3. **Acesse o container da aplicação**:
    ```bash
    docker compose run --rm app
    ```
    Isso vai criar um container temporário da aplicação.

### Instalação sem docker
```bash
python -m venv .venv

# Windows
.venv\Scripts\activate
pip install -r requirements-windows.txt 

# Linux
source .venv/bin/activate
pip install -r requirements-docker.txt
```
Se preferir executar sem Docker, crie um ambiente virtual e instale as dependências. Será necessário configurar as variáveis de ambiente de acordo com seus serviços Weaviate e Ollama locais.
## Configurações

As configurações são gerenciadas via variáveis de ambiente no arquivo `config.py`. Você pode sobrescrever os valores padrão definindo variáveis de ambiente num arquivo `.env`.

### Variáveis de Configuração
- **OLLAMA_CHAT_MODEL**: Modelo de chat do Ollama (padrão: `qwen3:4b-instruct-2507-q4_K_M`).
- **OLLAMA_EMBEDDING_MODEL**: Modelo de embedding (padrão: `embeddinggemma`).
- **OLLAMA_BASE_URL**: URL base do Ollama (padrão: `http://ollama:11434`).
- **WEAVIATE_HOST**: Host do Weaviate (padrão: `weaviate`).
- **WEAVIATE_HTTP_PORT**: Porta HTTP do Weaviate (padrão: `8080`).
- **WEAVIATE_GRPC_PORT**: Porta gRPC do Weaviate (padrão: `50051`).
- **INDEX_NAME**: Nome do índice no Weaviate (padrão: `Docs`).
- **MIN_CHUNKING_SIZE**: Tamanho mínimo dos chunks (padrão: `50`).

## Uso

1. **Inicie a aplicação** conforme os passos de instalação (`docker compose run --rm app` se estiver usando Docker).

2. **Loop de Upload de Documentos**:
    - No prompt inicial, digite URLs de documentos para fazer o chunking e armazenar.
    - Pressione ENTER com o input vazio para prosseguir ao chat.

3. **Loop Chat**:
    - Faça perguntas sobre o conteúdo dos documentos carregados.
    - Digite `sair` para encerrar.

### Exemplo de Sessão
```
Fazer upload de documentos para embedding.
Digite a URL do documento (ou apenas ENTER para ir ao chat): https://exemplo.com/documento.pdf
Documento salvo!

-- Assistente Governanca de Dados --
Digite 'sair' para encerrar.

Você: <Prompt>
Assistente: <Resposta>
```

## Dependências
- **LangChain**: Para construção de chains de IA.
- **Weaviate**: Cliente para banco vetorial.
- **Ollama**: Cliente para modelos de IA locais.
- **Docling**: Para processamento de documentos.

Para execução em container, todas as dependências são listadas em `requirements-docker.txt`.

## Estrutura do Projeto
```
file-rag-agent/
├── config.py                   # Configurações e variáveis de ambiente
├── main.py                     # Ponto de entrada da aplicação
├── save_doc.py                 # Chama o chunking e salva documentos
├── requirements-windows.txt    # Dependências para ambientes Windows
├── requirements-docker.txt     # Dependências para o container ou ambiente Linux
├── agent/
│   ├── core.py                 # Modelos e retriever
│   ├── chain.py                # Definição da chain RAG
│   └── __init__.py
├── rag/
│   ├── chunking.py             # Lógica de chunking
│   ├── embedding.py            # Incorporação e armazenamento
│   └── __init__.py
└── README.md
```

## Decisões Técnicas
### Modelos Padrão
- **Qwen3-4B**: Modelo adequado para a aplicação, com um tamanho mais enxuto e que cobre o escopo do chat, provendo respostas mais rápidas e ocupando menos espaço.
- **Embeddinggemma**: É mantido pela Google e possui um tamanho reduzido, mesmo que existem outras opções menores, esse modelo possui um ótimo desempenho pra seu tamanho.

### Código Modular
O código foi escrito modularizando toda seção que havia uma resposabilidade própria ou configuração particular (Ex.: Embedding e Chunking). Isso facilita a manutenção e escalabilidade. Caso haja a necessidade de criar uma interface web, via Streamlit por exemplo, é possível reutilizar várias funções já presentes.

### Pacote por Feature
Cada pacote representa uma feature do projeto (Agent, Rag), caso fosse criada uma interface web ou uma funcionalidade de scraping, um novo pacote correspondente seria criado.

### Upload de Arquivos em Execução
A decisão de adicionar na execução do programa principal a interação de realizar embedding dos arquivos foi tomada para centralizar o uso. Como a escala atual é reduzida, não há a necessidade de criar um ponto de entrada diferente.
