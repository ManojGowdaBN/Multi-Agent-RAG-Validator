from orchestration.lcel_pipeline import agentic_rag_chain

def test_lcel_pipeline():
    query = "Do the experimental results contradict the reported accuracy?"

    response = agentic_rag_chain.invoke(
        {"query": query}
    )

    print("\n FINAL SYSTEM RESPONSE\n")
    print(response)


if __name__ == "__main__":
    test_lcel_pipeline()
