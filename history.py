import config_ollama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.prompts import MessagesPlaceholder
from langchain.chains import create_retrieval_chain
from langchain.chains.history_aware_retriever import create_history_aware_retriever

def history(chain, retriever):
    # prompt used to process the query before sending it to the vectordatabase
    retriever_prompt = ChatPromptTemplate.from_messages([
        # Used as a placeholder for list of messages
        MessagesPlaceholder(variable_name = "chat_history"),
        ("human", "{input}"),
        ("human", "Given the above conversation, generate a search query to look"
        "up in order to get information relevant to the conversation. Avoid"
        "repeating information already mentioned in the conversation unless"
        "necessary for clarity.")
    ]
    )

    # retriever with integrated history, to call up data from the vectordatabase
    history_aware_retriever = create_history_aware_retriever(
        llm = config_ollama.llm,
        retriever = retriever,
        prompt = retriever_prompt
    )

    # puts together the document chain an the retriever
    retrieval_chain = create_retrieval_chain(
        history_aware_retriever,
        chain
    )
    return retrieval_chain