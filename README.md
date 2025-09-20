# Protoypical chatbot for querying library data with Lanchain
Dieses Projekt verwendet LangChain (Copyright © 2025 LangChain, Inc.) und
Streamlit (© 2025 Snowflake Inc) und enthält Code aus Tutorials, die unter
MIT-Lizenz oder der Apache 2.0 Lizenz stehen.
Eigenentwicklungen stehen unter MIT-Lizenz.

## Table of Contents
1. Project Description
2. Installation
3. Usage

## Project Description
This project contains a demo chatbot to query library data.

## Installation
Ollama (ollama pull for models)
- LLM: llama3.1:8b-instruct-q8_0
- Emedding: mxbai-embed-large:335m

OpenAI (Use OpenAI API)
- LLM: gpt-4.1-nano
- Embedding: text-embedding-3-small
    
Python dependencies (pip install *)
- faiss-cpu
- rank_bm25
- rank_bm25 nltk
- langchain
- langchain_core
- langchain_community
- langchain_ollama
- langchain_openai
- python-dotenv
- streamlit
- jq

## Usage
If you pull the directory on your computer you can start the program with:
streamlit run st_app.py.
For a succesful execution you have to use local Ollama or OpenAI with the
environment varibles.







