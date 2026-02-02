from typing import Dict, Any

from langchain_core.runnables import RunnableLambda, RunnablePassthrough

from agents.query_understanding_agent import QueryUnderstandingAgent
from agents.document_routing_agent import DocumentRoutingAgent
from agents.retrieval_agent import RetrievalAgent
from agents.fact_check_agent import FactCheckAgent
from agents.response_composition_agent import ResponseCompositionAgent


def build_agentic_pipeline(vectorstore):
    """
    Builds the full agentic RAG pipeline using LCEL.
    """

    # Initialize agents
    query_agent = QueryUnderstandingAgent()
    routing_agent = DocumentRoutingAgent()
    retrieval_agent = RetrievalAgent(vectorstore)
    fact_check_agent = FactCheckAgent()
    response_agent = ResponseCompositionAgent()

    
    # Runnable 1: Query Understanding
    
    query_understanding = RunnableLambda(
        lambda x: {
            **x,
            "query_type": query_agent.classify(x["query"])
        }
    )

   
    # Runnable 2: Document Routing
    
    document_routing = RunnableLambda(
        lambda x: {
            **x,
            "allowed_docs": routing_agent.route(x["query_type"])
        }
    )

    
    # Runnable 3: Retrieval
    
    retrieval = RunnableLambda(
        lambda x: {
            **x,
            "retrieved_docs": retrieval_agent.retrieve(
                query=x["query"],
                allowed_doc_types=x["allowed_docs"]
            )
        }
    )

    
    # Runnable 4: Fact Check
    
    fact_check = RunnableLambda(
        lambda x: {
            **x,
            "fact_result": fact_check_agent.evaluate(
                x["query"],
                x["retrieved_docs"]
            )
        }
    )

    
    # Runnable 5: Response Composition
    
    response_composition = RunnableLambda(
        lambda x: _compose_final_response(
            x["query"],
            x["fact_result"],
            response_agent
        )
    )

    
    # Full Agentic Pipeline
    
    agentic_pipeline = (
        RunnablePassthrough()
        | query_understanding
        | document_routing
        | retrieval
        | fact_check
        | response_composition
    )

    return agentic_pipeline


def _compose_final_response(query: str, fact_result: str, response_agent):
    """
    Helper to parse fact-check output and compose final response.
    """

    lines = fact_result.splitlines()

    verdict = lines[0]
    explanation = lines[1].replace("Explanation:", "").strip()
    sources = lines[2].replace("Sources:", "").strip()

    return response_agent.compose(
        query=query,
        verdict=verdict,
        explanation=explanation,
        sources=sources
    )
