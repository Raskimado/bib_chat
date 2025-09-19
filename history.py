"""This module ensures that the latest query is made taking into account the
previous dialog.

Functions:
- history(chain, retriever): Creates new queries to retrieve documents and
returns the retriever chain.
"""

__file__ = "history.py"
__version__ = "0.1"
__author__ = "Martin Brossard"
__copyright__ = "Copyright (C) 2025 Martin Brossard"
__license__ = "MIT"

import config_ollama

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.prompts import MessagesPlaceholder
from langchain.chains.retrieval import create_retrieval_chain
from langchain.chains.history_aware_retriever import (
    create_history_aware_retriever,
)


def history(chain, retriever):
    """Create a new query based on the previous conversation. Use the new query
    to retrieve documents from the vetorstore. Create a retrieval chain and
    retrun it.

    Keyword arguments:
    chain -- hands over the stuff_document_chain
    retriever -- hands over the retriever for the search
    """

    history_prompt = ChatPromptTemplate.from_messages([
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}"),
        ("human", "Based on the above conversation, generate a search query to"
        "find relevant information. Avoid repeating information already"
        "mentioned in the conversation unless necessary for clarity.")
    ]
    )

    history_aware_retriever = create_history_aware_retriever(
        llm=config_ollama.llm,
        retriever=retriever,
        prompt=history_prompt
    )

    retrieval_chain = create_retrieval_chain(
        history_aware_retriever,
        chain
    )
    return retrieval_chain

