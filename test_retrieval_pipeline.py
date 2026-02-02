from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings

from agents.retrieval_agent import RetrievalAgent


FAISS_INDEX_PATH = "vectorstore/faiss_test_index"


def test_retrieval_agent():
    print("🔹 Loading FAISS index...")
    embeddings = OpenAIEmbeddings()

    vectorstore = FAISS.load_local(
        FAISS_INDEX_PATH,
        embeddings,
        allow_dangerous_deserialization=True
    )

    retrieval_agent = RetrievalAgent(vectorstore)

    
    # Test queries
    
    test_cases = [
        {
            "query": "What is the reported accuracy?",
            "allowed_doc_types": ["excel"],
            "allowed_sections": ["results"]
        },
        {
            "query": "Explain the transformer architecture",
            "allowed_doc_types": ["pdf", "ppt"],
            "allowed_sections": None
        },
        {
            "query": "Do the results contradict the experiment logs?",
            "allowed_doc_types": ["pdf", "excel", "text"],
            "allowed_sections": None
        }
    ]

    for i, case in enumerate(test_cases, start=1):
        print("\n" + "=" * 60)
        print(f" Test Case {i}")
        print("Query:", case["query"])

        docs = retrieval_agent.retrieve(
            query=case["query"],
            top_k=5,
            allowed_doc_types=case["allowed_doc_types"],
            allowed_sections=case["allowed_sections"]
        )

        print(f" Retrieved {len(docs)} documents")

        for d in docs:
            print("-" * 40)
            print("Content (first 200 chars):")
            print(d.page_content[:200])
            print("Metadata:", d.metadata)


if __name__ == "__main__":
    test_retrieval_agent()
