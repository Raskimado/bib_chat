import config_ollama
from history import history
from load_text import adapt_text
from langchain.chains.combine_documents import create_stuff_documents_chain
#from langchain_core.output_parsers import StrOutputParser
from langchain.schema import Document
#from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.messages import HumanMessage, AIMessage

chat_history = []

#indexing - load
titles = adapt_text()
def load_documents():
    #Load file from path
    # loader = TextLoader(
    #     file_path = "ergebnisse.txt",
    #     encoding = "utf-8")
    # docs = loader.load()
    # In ein Document-Objekt umwandeln
    docs = [Document(page_content = titles)]
    return docs

#indexing - split
def split_documents(docs):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )
    chunks = text_splitter.split_documents(docs)
    #print(f"number of chunks {len(chunks)}")
    #print(chunks[1].page_content)
    return chunks

#convert documents to vectors amd save in vectorstore, call embedding model 
def load_embeddings(documents):
    embeddings = OllamaEmbeddings(
        model="nomic-embed-text:v1.5",
        base_url="https://ollama-mabr1938.apps.rhos.th-wildau.de:443"
    )
    vdatabase = Chroma.from_documents(documents, embeddings)
    print(vdatabase._collection.count())
    # query = "150 Jahre Viscom"
    # ergebnisse = vdatabase.similarity_search(query)
    # print(ergebnisse)
    # all_docs = vdatabase.get()
    #print(all_docs)
    return vdatabase

# Create chain for the request
def create_chain(vdatabase):
    # initialize model and define prompt via function call from config_ollama.py
    llm = config_ollama.llm
    prompt = config_ollama.prompt
    
    chain = create_stuff_documents_chain(
        llm,
        prompt
    )
    retriever = vdatabase.as_retriever(search_kwargs={"k": 10})

    # import history function from history.py
    retrieval_chain = history(chain, retriever)
    return retrieval_chain

# Due to the retrieval_chain calls for relevant data based on query and history
def generate_response(retrieval_chain, query, chat_history):
    response = retrieval_chain.invoke({
        "input": query,
        "chat_history": chat_history
    })
    return response["answer"]

def query(query):
    docs = load_documents()
    chunks = split_documents(docs)
    vdatabase = load_embeddings(chunks)
    retrieval_chain = create_chain(vdatabase)
    response = generate_response(retrieval_chain, query, chat_history)

    # adds the content from the query and the response to the chat_history
    # befor the next question
    chat_history.append(HumanMessage(content=query))
    chat_history.append(AIMessage(content=response))
    
    return response