"""This module generates multiple query based on the orignal query. This should
lead to more diversity in the output of the retriever.

Class:
LineListOutputParser(BaseOutputParser[List[str]]): Output parse for a list of
lines.

Functions:
- parse(self, text: str) -> List[str]: Splits list into queries.
- multi-query(): Defines task to generate multiple queries.

"""

__file__ = "multi_query.py"
__version__ = "0.1"
__author__ = "Martin Brossard"
__copyright__ = "Copyright (C) 2025 Martin Brossard"
__license__ = "MIT"

from typing import List
from langchain_core.output_parsers import BaseOutputParser
from langchain_ollama import OllamaLLM
from langchain_core.prompts import PromptTemplate


class LineListOutputParser(BaseOutputParser[List[str]]):
    """Output parser for a list of lines."""

    def parse(self, text: str) -> List[str]:
        """Split the LLM result into a list of queries"""
        lines = text.strip().split("\n")
        return list(filter(None, lines))  # Remove empty lines


def multi_query():
    """Define the LLM and the prompt and return the chain for processing."""
    llm = OllamaLLM(
        model="llama3.1:8b",
        temperature=0.01,
        )
    output_parser = LineListOutputParser()

    QUERY_PROMPT = PromptTemplate(
        input_variables=["question"],
        template="""You are an AI language model assistant. Your task is to
        generate two different versions of the given user question to retrieve
        relevant documents from a vectoredatabase. By generating multiple
        perspectives on the user question, your goal is to help the user
        overcome some of the limitations of the distance-based similarity
        search. Provide these alternative questions separated by newlines.
        Generate only closely related paraphrases
        Original question: {question}""",
    )
    
    llm_chain = QUERY_PROMPT | llm | output_parser
    return llm_chain

   