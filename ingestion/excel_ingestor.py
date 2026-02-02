from pathlib import Path
from typing import List
import pandas as pd

from langchain_core.documents import Document


class ExcelIngestor:
    def __init__(self, excel_dir: Path):
        self.excel_dir = excel_dir

    def ingest(self) -> List[Document]:
        documents = []

        for file in self.excel_dir.glob("*.xlsx"):
            try:
                df = pd.read_excel(file, sheet_name=None)
                for sheet, data in df.items():
                    text = data.astype(str).fillna("").to_string()
                    documents.append(
                        Document(
                            page_content=text,
                            metadata={
                                "document_type": "xlsx",
                                "source": file.name,
                                "section": f"sheet:{sheet}",
                            },
                        )
                    )
            except Exception as e:
                print(f" Failed to ingest {file.name}: {e}")

        return documents
