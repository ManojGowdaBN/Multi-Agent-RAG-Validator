from typing import Dict
from langchain_core.runnables import RunnableLambda, RunnablePassthrough

from vectorstore.faiss_loader import load_faiss_index
from agents.query_understanding_agent import QueryUnderstandingAgent
from agents.document_routing_agent import DocumentRoutingAgent
from agents.retrieval_agent import RetrievalAgent
from agents.fact_check_agent import FactCheckAgent
from agents.response_composition_agent import ResponseCompositionAgent


def build_agentic_rag_chain(faiss_dir: str):

    vectorstore = load_faiss_index(faiss_dir)

    query_agent = QueryUnderstandingAgent()
    routing_agent = DocumentRoutingAgent()
    retrieval_agent = RetrievalAgent(vectorstore)
    fact_check_agent = FactCheckAgent()
    response_agent = ResponseCompositionAgent()

    def understand_query(inputs: Dict) -> Dict:
        return {**inputs, "query_type": query_agent.classify(inputs["query"])}

    def route_documents(inputs: Dict) -> Dict:
        return {
            **inputs,
            "allowed_doc_types": routing_agent.route(inputs["query_type"])
        }

    def retrieve_documents(inputs: Dict) -> Dict:
        docs = retrieval_agent.retrieve(
            query=inputs["query"],
            top_k=5,
            allowed_doc_types=inputs["allowed_doc_types"],
            allowed_sections=None
        )
        return {**inputs, "documents": docs}

    def fact_check(inputs: Dict) -> Dict:
        result = fact_check_agent.check(
            inputs["query"],
            inputs["documents"]
        )
        return {**inputs, "fact_check_result": result}

    def compose_response(inputs: Dict) -> str:
        return response_agent.compose(
            query=inputs["query"],
            documents=inputs["documents"],
            fact_check_result=inputs["fact_check_result"]
        )

    return (
        RunnablePassthrough()
        | RunnableLambda(understand_query)
        | RunnableLambda(route_documents)
        | RunnableLambda(retrieve_documents)
        | RunnableLambda(fact_check)
        | RunnableLambda(compose_response)
    )
