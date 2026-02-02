from typing import List
from pathlib import Path

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS

from ingestion.pdf_ingestor import PdfIngestor
from ingestion.docx_ingestor import DocxIngestor
from ingestion.text_ingestor import TextIngestor
from ingestion.ppt_ingestor import PPTIngestor
from ingestion.excel_ingestor import ExcelIngestor


class IngestionPipeline:
    def __init__(
        self,
        data_dir: str = "data",
        faiss_dir: str = "vectorstore/faiss_index",
    ):
        self.data_dir = Path(data_dir)
        self.faiss_dir = faiss_dir

        self.embeddings = OpenAIEmbeddings()
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=800,
            chunk_overlap=150,
        )

    def run(self):
        print(" Starting ingestion pipeline")

        documents: List = []

        
        # Ingest documents
       
        pdf_docs = PdfIngestor(self.data_dir / "pdf").ingest()
        docx_docs = DocxIngestor(self.data_dir / "docx").ingest()
        txt_docs = TextIngestor(self.data_dir / "texts").ingest()
        ppt_docs = PPTIngestor(self.data_dir / "ppts").ingest()
        excel_docs = ExcelIngestor(self.data_dir / "excels").ingest()

        
        # Logging
        
        print(f" PDFs   : {len(pdf_docs)}")
        print(f" DOCX  : {len(docx_docs)}")
        print(f" TXT   : {len(txt_docs)}")
        print(f" PPT   : {len(ppt_docs)}")
        print(f" EXCEL : {len(excel_docs)}")

        documents.extend(
            pdf_docs
            + docx_docs
            + txt_docs
            + ppt_docs
            + excel_docs
        )

        if not documents:
            raise RuntimeError("No documents found for ingestion")

        
        # Chunking
        
        chunks = self.splitter.split_documents(documents)
        chunks = [c for c in chunks if c.page_content.strip()]

        print(f" Total chunks created: {len(chunks)}")

        
        # Vector store
        
        vectorstore = FAISS.from_documents(chunks, self.embeddings)
        vectorstore.save_local(self.faiss_dir)

        print(f" FAISS index saved to {self.faiss_dir}")
