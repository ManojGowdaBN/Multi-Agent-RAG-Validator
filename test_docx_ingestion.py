# test_docx_ingestion.py
from ingestion.docx_ingestor import DocxIngestor

def test_docx_ingestion():
    ingestor = DocxIngestor(docx_dir="data/docx") 
    docs = ingestor.ingest()

    print(f"Ingested {len(docs)} DOCX documents")

    for d in docs:
        print(d.metadata)
        print(d.page_content[:400])

if __name__ == "__main__":
    test_docx_ingestion()
