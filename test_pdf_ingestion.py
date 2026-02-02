from ingestion.pdf_ingestor import ingest_pdfs

def test_pdf_ingestion():
    docs = ingest_pdfs()

    print(f"\nTotal Documents Loaded: {len(docs)}")

    if len(docs) > 0:
        print("\nSample Document:")
        print("Content (first 300 chars):")
        print(docs[0].page_content[:300])

        print("\nMetadata:")
        print(docs[0].metadata)

if __name__ == "__main__":
    test_pdf_ingestion()
