# test_ppt_ingestion.py

from ingestion.ppt_ingestor import PPTIngestor

def test_ppt_ingestion():
    ingestor = PPTIngestor("data/ppts")
    docs = ingestor.ingest()

    print(f"Loaded {len(docs)} ppt documents")

    if docs:
        sample = docs[0]
        print("\nSample Document:")
        print("Content (first 300 chars):")
        print(sample.page_content[:300])
        print("\nMetadata:")
        print(sample.metadata)


if __name__ == "__main__":
    test_ppt_ingestion()
