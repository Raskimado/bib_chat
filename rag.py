"""This module represents the RAG process

Functions:
- load_documents(): Loads data basis from load_text.py.
- split_documents(docs): Splits the databasis into chunks.
- load_embeddings(chunks): Creates a vectorstore.
- create_chain(llm_chain, chunks, vdatabase): Creates a retrieval chain.
- generate_response(retrieval_chain, query, chat_history): Invokes the retrieval
chain.
- get_vdatabase(_chunks): returns the vetorstore to cache the results.
- query(query): Calls all relevant functions.
"""

__file__ = "rag.py"
__version__ = "0.1"
__author__ = "Martin Brossard"
__copyright__ = "Copyright (C) 2025 Martin Brossard"
__license__ = "MIT"

import streamlit as st
import nltk
import logging

import config_ollama

from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.output_parsers import StrOutputParser
from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from langchain.retrievers.multi_query import MultiQueryRetriever
from langchain_community.vectorstores import FAISS
from langchain_community.retrievers import BM25Retriever
from langchain.retrievers import EnsembleRetriever
from langchain_core.messages import HumanMessage, AIMessage
from nltk.tokenize import word_tokenize
from encodings.idna import dots

from load_text import adapt_text, load_json
from multi_query import multi_query
from history import history

nltk.download("punkt_tab") 

chat_history = []


def load_documents():
    """Convert the data basis into the langchain document format and return the
    docs.
    """
    docs = []
    results = load_json()
    titles = adapt_text(results)
    for title in titles:
        doc = Document(page_content = title)
        docs.append(doc)
    # print(docs)
    return docs


def split_documents(docs):
    """Split the whole data into chunks and return them
    
    Keyword arguments:
    docs - hands over docs in the langchain document format
    """
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size = 256,
        chunk_overlap = 50,
        )
    chunks = text_splitter.split_documents(docs)
    print(f"number of chunks {len(chunks)}")
    # print(chunks[2])
    return chunks


def load_embeddings(chunks):
    """Convert the chunks to vectors and save them in the vectorstore
    
    Keyword arguments:
    chunks -- hands over the split documents
    """
    embeddings = OllamaEmbeddings(
        model="mxbai-embed-large:335m",
    )
    vdatabase = FAISS.from_documents(
        chunks,
        embeddings,
        )

    # query = "I am looking for e-journals about innovation."
    # ergebnisse = vdatabase.similarity_search(query)
    # print("FAISS", ergebnisse)
    # all_docs = vdatabase.get()
    # print(all_docs)
    return vdatabase


def create_chain(llm_chain, chunks, vdatabase):
    """Import LLM and prompt. Create a document chain and a retreiver. Finally,
    return an retrieval chain.

    Keyword arguments:
    llm_chain -- hands over the chain to create multiple queries
    chunks -- hands over split documents
    vdatabase -- hands over the vectorstore
    """
    llm = config_ollama.llm
    prompt = config_ollama.prompt
    output_parser = StrOutputParser()
    
    chain = create_stuff_documents_chain(
        llm,
        prompt,
        output_parser=output_parser
    )
    faiss_retriever = vdatabase.as_retriever(
        search_type="similarity_score_threshold",
        search_kwargs={"score_threshold": 0.4, "k": 3}
        )
    
    retriever = MultiQueryRetriever(
        retriever=faiss_retriever,
        llm_chain=llm_chain,
        )
    logging.basicConfig()
    logging.getLogger("langchain.retrievers.multi_query").setLevel(logging.INFO)

    bm25_retriever = BM25Retriever.from_documents(
        chunks,
        k=2,
        preprocess_func=word_tokenize,
        )
    # results = bm25_retriever.invoke("I am looking for e-journals about innovation.")
    # for doc in results:
    #     print("BM25", doc.page_content)

    ensemble_retriever = EnsembleRetriever(
        retrievers=[bm25_retriever, retriever], weights=[0.5, 0.5]
        )

    # import history aware retriever
    retrieval_chain = history(chain, ensemble_retriever)
    return retrieval_chain


def generate_response(retrieval_chain, query, chat_history):
    """Invoke the query and return the generated response.
    
    Keyword arguments:
    retrieval_chain -- hands over the retrieval chain to invoke
    query -- hands over the current query
    chat_history -- hands over the previous dialog
    """
    prefixed_query = f"""Represent this sentence for searching relevant
    passages: {query}"""
    response = retrieval_chain.invoke({
        "input": prefixed_query,
        "chat_history": chat_history
    })
    r = response["context"]
    print(r)
    response = response["answer"]
    
    # adds the content from the query and the response to the chat_history
    chat_history.append(HumanMessage(content=query))
    chat_history.append(AIMessage(content=response))

    return response


@st.cache_resource
def get_vdatabase(_chunks):
    """Return the vetorstore an save it as the cache.
    
    Keyword arguments:
    chunks -- hands over split documents
    """
    vdatabase = load_embeddings(_chunks)
    return vdatabase


def query(query):
    """Call all functions and return the response
    
    Keyword arguments:
    query -- hands over the current query
    """
    query = query.lower()
    docs = load_documents()
    chunks = split_documents(docs)
    vdatabase = get_vdatabase(chunks)
    llm_chain = multi_query()
    retrieval_chain = create_chain(llm_chain, chunks, vdatabase)
    response = generate_response(retrieval_chain, query, chat_history)
    return response
