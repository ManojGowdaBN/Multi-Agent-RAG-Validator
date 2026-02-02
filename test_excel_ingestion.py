from ingestion.excel_ingestor import ExcelIngestor


def test_excel_ingestion():
    ingestor = ExcelIngestor(data_dir="data/excels")
    docs = ingestor.load()

    print(f"Loaded {len(docs)} excel documents")

    if docs:
        sample = docs[0]
        print("\nSample Document:")
        print("Content (first 300 chars):")
        print(sample.page_content[:300])
        print("\nMetadata:")
        print(sample.metadata)


if __name__ == "__main__":
    test_excel_ingestion()
