# Protoypical chatbot for querying library data with Lanchain
## Table of Contents
1. Project Description
2. Installation
3. Usage

## Project Description
This project contains a demo chatbot to query library data.

## Installation
Ollama (ollama pull for models)
    LLM: llama3:8b
    Emedding: nomic-embed-text:v1.5
    
Python dependencies (pip install *)
- chromadb
- langchain
- langchain_core
- langchain_community
- lanchain_ollama
- streamlit

## Usage
If you pull the directory on your computer you can start the program with:
streamlit run st_app.py
For a succesful execution you have to be within the campus network of the
Technical University of Applied Sciences Wildau otherwise use local Ollama.
