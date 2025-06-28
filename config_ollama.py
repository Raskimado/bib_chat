from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.prompts import MessagesPlaceholder

#initialize model
llm = OllamaLLM(
    model="llama3:8b",
    base_url="https://ollama-mabr1938.apps.rhos.th-wildau.de:443",
    temperature=0.4,
)

#define prompt
prompt = ChatPromptTemplate.from_messages(
    [
    ("system", "Answer the user's questions based on the context: {context}."
    "Be concise but use at least on sentence."
    "Based on the context, the response should contain three titles."
    "If you do not find titles based on the context, say it accordingly."
    "Never mention the MMS-ID."),
    # Used as a placeholder for list of messages
    MessagesPlaceholder(variable_name = "chat_history"),
    ("human", "{input}")
    ]
)