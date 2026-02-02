from vectorstore.faiss_loader import load_faiss_index
from agents.retrieval_agent import RetrievalAgent
from agents.fact_check_agent import FactCheckAgent
from agents.response_composition_agent import ResponseCompositionAgent


def test_response_composition():
    vectorstore = load_faiss_index("vectorstore/faiss_test_index")

    retrieval_agent = RetrievalAgent(vectorstore)
    fact_check_agent = FactCheckAgent()
    response_agent = ResponseCompositionAgent()

    query = "Do the experimental results contradict the reported accuracy?"

    retrieved_docs = retrieval_agent.retrieve(
        query=query,
        top_k=5,
        allowed_doc_types=["excel"],
        allowed_sections=["results"]
    )

    fact_check_result = fact_check_agent.check(query, retrieved_docs)

    final_answer = response_agent.compose(
        query=query,
        fact_check_result=fact_check_result
    )

    print("FINAL RESPONSE\n")
    print(final_answer)


if __name__ == "__main__":
    test_response_composition()
