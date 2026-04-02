from config import OLLAMA_CHAT_MODEL
from agent.core import get_chat_model

from langchain_core.vectorstores import VectorStoreRetriever
from langchain_core.runnables import RunnablePassthrough, RunnableSerializable
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_ollama import ChatOllama

SYSTEM_PROMPT = """Você é um assistente para alunos de faculdade.
Regras:
- Responda sempre em português.
- Se não souber a resposta, diga que não sabe.
- Se não se lembrar do contexto, diga que não sabe.
- Seja educado.

Contexto recuperado:
{context}""" # Contexto obtido através do rag

def get_chain(retriever: VectorStoreRetriever, chat_model: ChatOllama) -> RunnableSerializable:

    prompt = ChatPromptTemplate.from_messages([
        ("system", SYSTEM_PROMPT),
        ("human", "{question}"),
    ])

    # Define a chain
    chain = (
        {"context": retriever, "question": RunnablePassthrough()}
        | prompt
        | chat_model
        | StrOutputParser()
    )
    return chain