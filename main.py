from dotenv import load_dotenv
load_dotenv()

from langchain_openai import OpenAIEmbeddings
from langchain_core.documents import Document
from langchain_community.vectorstores import FAISS

from orchestration.agent_orchestrator import build_agentic_pipeline



def main():
    # Simulated ingested documents
    docs = [
        Document(
            page_content="Accuracy achieved was 92.3 percent.",
            metadata={"document_type": "excel", "section": "results"}
        ),
        Document(
            page_content="Experiment logs indicate accuracy fluctuated around 85 percent.",
            metadata={"document_type": "txt", "section": "notes"}
        ),
    ]

    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.from_documents(docs, embeddings)

    pipeline = build_agentic_pipeline(vectorstore)

    response = pipeline.invoke({
        "query": "What is the accuracy value reported?"
    })

    print("AGENTIC PIPELINE OUTPUT")
    print("=" * 70)
    print(response)


if __name__ == "__main__":
    main()
