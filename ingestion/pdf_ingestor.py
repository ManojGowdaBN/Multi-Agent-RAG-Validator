from pathlib import Path
from typing import List

from langchain_core.documents import Document
from langchain_community.document_loaders import PyPDFLoader


class PdfIngestor:
    def __init__(self, pdf_dir: Path):
        self.pdf_dir = pdf_dir

    def ingest(self) -> List[Document]:
        documents: List[Document] = []

        if not self.pdf_dir.exists():
            return documents

        for pdf_file in self.pdf_dir.glob("*.pdf"):
            try:
                loader = PyPDFLoader(str(pdf_file))
                pages = loader.load()

                for page in pages:
                    page.metadata.update(
                        {
                            "document_type": "pdf",
                            "source": pdf_file.name,
                            "section": f"page_{page.metadata.get('page', 0) + 1}",
                        }
                    )

                documents.extend(pages)

            except Exception as e:
                print(f"Failed to ingest {pdf_file.name}: {e}")

        return documents
