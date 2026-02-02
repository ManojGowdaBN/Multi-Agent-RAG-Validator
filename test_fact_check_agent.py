from vectorstore.faiss_loader import load_faiss_index
from agents.retrieval_agent import RetrievalAgent
from agents.fact_check_agent import FactCheckAgent


def test_fact_check():
    vectorstore = load_faiss_index("vectorstore/faiss_test_index")

    retrieval_agent = RetrievalAgent(vectorstore)
    fact_check_agent = FactCheckAgent()

    query = "Do the experimental results contradict the reported accuracy?"

    retrieved_docs = retrieval_agent.retrieve(
        query=query,
        top_k=5,
        allowed_doc_types=["excel"],
        allowed_sections=["results"]
    )

    result = fact_check_agent.check(query, retrieved_docs)

    print("\n🔍 FACT CHECK RESULT\n")
    print(result["analysis"])
    print("\nSources:")
    for s in result["sources"]:
        print(s)


if __name__ == "__main__":
    test_fact_check()
