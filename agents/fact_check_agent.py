from dotenv import load_dotenv
load_dotenv()

from typing import List, Dict

from langchain_core.documents import Document
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate


class FactCheckAgent:
    """
    Cross-verifies claims using retrieved documents
    and determines consistency / contradiction.
    """

    def __init__(self, model: str = "gpt-4o-mini", temperature: float = 0.0):
        self.llm = ChatOpenAI(
            model=model,
            temperature=temperature
        )

        self.prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "You are an academic research validation agent. "
                    "Your task is to fact-check claims using provided evidence. "
                    "Detect contradictions, inconsistencies, or support. "
                    "Be precise and conservative. Do not hallucinate."
                ),
                (
                    "human",
                    """
Claim / Question:
{query}

Retrieved Evidence:
{evidence}

Instructions:
1. Compare numeric values if present.
2. Detect contradictions across documents.
3. Decide one verdict:
   - SUPPORTED
   - CONTRADICTED
   - PARTIALLY_SUPPORTED
4. Provide a short justification.
5. List key evidence sources.
"""
                )
            ]
        )

    def _format_evidence(self, documents: List[Document]) -> str:
        """
        Converts retrieved documents into a readable evidence block.
        """
        blocks = []

        for i, doc in enumerate(documents, start=1):
            meta = doc.metadata
            source = meta.get("source", "unknown")
            doc_type = meta.get("document_type", "unknown")

            blocks.append(
                f"[Evidence {i}] ({doc_type} | {source})\n"
                f"{doc.page_content}"
            )

        return "\n\n".join(blocks)

    def check(self, query: str, documents: List[Document]) -> Dict:
        """
        Perform fact-checking over retrieved documents.
        """

        if not documents:
            return {
                "verdict": "INSUFFICIENT_EVIDENCE",
                "confidence": "Low",
                "justification": "No documents were retrieved for validation.",
                "sources": []
            }

        evidence_text = self._format_evidence(documents)

        chain = self.prompt | self.llm

        response = chain.invoke(
            {
                "query": query,
                "evidence": evidence_text
            }
        )

        return {
            "verdict": "SEE_RESPONSE",
            "analysis": response.content,
            "sources": [
                {
                    "source": d.metadata.get("source"),
                    "document_type": d.metadata.get("document_type"),
                    "section": d.metadata.get("section"),
                }
                for d in documents
            ]
        }
