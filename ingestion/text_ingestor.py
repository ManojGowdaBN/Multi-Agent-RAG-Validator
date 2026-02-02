from pathlib import Path
from typing import List

from langchain_core.documents import Document


class TextIngestor:
    def __init__(self, text_dir: Path):
        self.text_dir = text_dir

    def ingest(self) -> List[Document]:
        documents: List[Document] = []

        if not self.text_dir.exists():
            return documents

        for txt_file in self.text_dir.glob("*.txt"):
            try:
                content = txt_file.read_text(encoding="utf-8", errors="ignore")

                if not content.strip():
                    continue

                doc = Document(
                    page_content=content,
                    metadata={
                        "document_type": "txt",
                        "source": txt_file.name,
                        "section": "full_document",
                    },
                )

                documents.append(doc)

            except Exception as e:
                print(f"Failed to ingest {txt_file.name}: {e}")

        return documents
