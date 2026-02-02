from dotenv import load_dotenv
load_dotenv()
from typing import List, Optional

from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document


class RetrievalAgent:
    """
    Retrieves relevant documents from FAISS using
    query + routing-based metadata filters.
    """

    def __init__(self, vectorstore: FAISS):
        self.vectorstore = vectorstore

    def retrieve(
        self,
        query: str,
        top_k: int = 5,
        allowed_doc_types: Optional[List[str]] = None,
        allowed_sections: Optional[List[str]] = None,
    ) -> List[Document]:
        """
        Perform similarity search with routing-aware metadata filtering.
        """

       
        # Build FAISS filter
        
        metadata_filter = {}

        if allowed_doc_types:
            metadata_filter["document_type"] = allowed_doc_types

        if allowed_sections:
            metadata_filter["section"] = allowed_sections

        
        # Create retriever
        
        retriever = self.vectorstore.as_retriever(
            search_kwargs={
                "k": top_k,
                "filter": metadata_filter if metadata_filter else None
            }
        )

        
        # Retrieve documents
       
        documents = retriever.invoke(query)

        return documents
