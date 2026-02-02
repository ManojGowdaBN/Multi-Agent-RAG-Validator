import os
from dotenv import load_dotenv

from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser

# Load environment variables ONCE when agent is initialized
load_dotenv()



class QueryUnderstandingAgent:
    """
    Classifies a user query into a specific query type.
    """

    def __init__(self, model_name="gpt-4o-mini"):
        self.llm = ChatOpenAI(model=model_name, temperature=0)

        self.prompt = PromptTemplate(
            input_variables=["query"],
            template="""
You are an AI agent responsible for classifying academic research queries.

Classify the following query into exactly ONE of these categories:
- conceptual
- evidence
- numeric
- contradiction

Query:
{query}

Respond with ONLY the category name.
"""
        )

        self.chain = self.prompt | self.llm | StrOutputParser()

    def classify(self, query: str) -> str:
        return self.chain.invoke({"query": query}).strip().lower()
