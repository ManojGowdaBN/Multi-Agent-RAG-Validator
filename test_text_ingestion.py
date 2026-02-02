from ingestion.text_ingestor import TextIngestor


def test_text_ingestion():
    ingestor = TextIngestor(text_dir="data/texts")
    documents = ingestor.ingest()

    print(f"Loaded {len(documents)} text documents\n")

    if documents:
        doc = documents[0]
        print("Sample Document:")
        print("Content (first 300 chars):")
        print(doc.page_content[:300])
        print("\nMetadata:")
        print(doc.metadata)


if __name__ == "__main__":
    test_text_ingestion()
