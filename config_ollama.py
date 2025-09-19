"""This module defines the LLM together with the system-prompt. The context,
user input, chat-history and examples from the technique few-shot learning are
part of the prompt.
"""

__file__ = "config_ollama.py"
__version__ = "0.1"
__author__ = "Martin Brossard"
__copyright__ = "Copyright (C) 2025 Martin Brossard"
__license__ = "MIT"

from langchain_ollama import OllamaLLM
from langchain_core.prompts import (
    ChatPromptTemplate,
    FewShotChatMessagePromptTemplate,
)
from langchain_core.prompts import MessagesPlaceholder

# from config_api import load_env

# # Load environment variables
# load_env()

llm = OllamaLLM(
    model="llama3.1:8b-instruct-q8_0",
    temperature=0.4,
)

examples = [
    {
        "question": "Do you have titles about architecture?",
        "answer": """
Here are some interesting titles about architecture that you might find usefull:

1.  Alpbeizli der Schweiz by Valerie Killeen \\\n Das Buch "Alpbeizli der 
Schweiz" bietet einen umfassenden Einblick in die Alpwirtschaft und die 
traditionelle Architektur der Schweiz, insbesondere in Bezug auf Almhütten und 
Sennhütten.

2.  Werdenberg Stadt im Mittelalter \\\n Das Buch behandelt die Geschichte und 
Entwicklung der Stadt Werdenberg in der Schweiz während des Mittelalters.

3.  Gartenführer Schweiz \\\n In diesem Buch geht es nicht direkt um Architektur 
sondern um Landschafsarchitekur. Der Gartenführer beschreibt die Vielfalt der 
Gärten in der Schweiz.

Let me know if you need more information or if you are looking for other 
information.
""",
    },
    {
        "question": "I'm looking for some interesting novels and nonfiction "
        "books to get into.",
        "answer": """
Hello! Here are three book recommendations for you:

1.  The Shadow of the Wind by Carlos Ruiz Zafón \\\n Set in the haunting streets 
of post-war Barcelona, this novel intertwines mystery and romance as a young 
boy discovers a forgotten book that changes his life forever.

2.  Sapiens: A Brief History of Humankind by Yuval Noah Harari \\\n This 
engaging nonfiction book provides a sweeping overview of human history, 
exploring how Homo sapiens came to dominate the earth through cognitive, 
agricultural, and scientific revolutions.

3.   The Midnight Library by Matt Haig \\\n Between life and death, in a 
library of infinite books, a woman explores the different lives she might have 
lived.

I hope you find these suggestions inspiring. Have a wonderful day and happy 
reading!"

""",
    },
    {
        "question": "Do you have titles about Tusnamis?",
        "answer": """
Here is a recommendation related to Tusnamis:

1.  Danger of Tusnmais by Edgar Ellen \\\n This books shows the impact of 
Tusnamis on infrastructure

Unfortunately, I do not have more information about Tusnamis or related titles 
at this time.
""",
    },
    {
        "question": "Do you have titles about riddles?",
        "answer": "Unfortunately, I could not find any titles on this topic.",
    },
] 

example_prompt = ChatPromptTemplate.from_messages(
    [
        ("human", "{question}"),
        ("ai", "{answer}"),
    ]
)

few_shot_prompt = FewShotChatMessagePromptTemplate(
    example_prompt=example_prompt,
    examples=examples,
)

# print(few_shot_prompt.invoke({}).to_messages())

#define prompt
prompt = ChatPromptTemplate.from_messages(
    [
    ("system",
    "You are a recommendation AI providing recommendations of books, e-books,"
    "print journals, and e-journals."

    "Answer the user's questions solely based on the provided context: "
    "{context}."  
    "Do not mention the context or retrieval process in your answer."
    "Be brief, concise, and friendly. Use at least one full sentence."

    "Search the provided context {context} carefully for relevant information"
    "to answer the user's question."
    "If you cannot find relevant information in the context, respond with one "
    "of the following exact phrases:"
    "- 'I don't know anything about it.'"
    "- 'I don't have that information.'"
    "- 'It's not contained in the context.'"
    "Do not answer based on any knowledge outside the given context or make"
    "assumptions."

    "Only recommend titles explicitly present in the context. Never recommend"
    "titles not found in {context}."
    "If multiple titles are found, provide up to three recommendations in a "
    "numbered"
    "list. Each number corresponds to exactly one title."
    "If fewer than three titles are found, list only those honestly."
    "If no titles are found, apologize and inform the user clearly that no "
    "suitable results are available."

    "Do not mention any MMS-IDs."
    "Only use numbered lists for listing titles. Do not use lists for other"
    "information."

    "Ask clarifying questions if needed to better understand the user's query."

    "Always end your response with a brief concluding statement that clearly"
    "summarizes or wraps up the information."
    ),
    MessagesPlaceholder(variable_name = "chat_history"),
    ("human", "{input}"),
    ]
)