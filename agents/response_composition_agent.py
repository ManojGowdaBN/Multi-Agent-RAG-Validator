from dotenv import load_dotenv
load_dotenv()

from typing import Dict, List
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.documents import Document


class ResponseCompositionAgent:
    """
    Converts retrieved documents + fact-check results
    into a clear, human-like, and well-grounded response,
    without hallucination or invented citations.
    """

    def __init__(self, model: str = "gpt-4o-mini", temperature: float = 0.3):
        self.llm = ChatOpenAI(
            model=model,
            temperature=temperature
        )

        
        self.prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    """
You are a knowledgeable and careful academic assistant.

Rules you MUST follow:
- Use ONLY the provided analysis and retrieved sources.
- Do NOT add external knowledge or assumptions.
- Do NOT invent facts, evidence, or citations.
- If the documents do not clearly support an answer, say so honestly.
- Write naturally, like a human expert explaining to another human.
"""
                ),
                (
                    "human",
                    """
User Question:
{query}

Document-Based Analysis:
{analysis}

Retrieved Evidence:
{sources}

Response Guidelines:
- Start with a clear, direct answer in natural language.
- Explain the answer briefly using the document-based analysis.
- If there are limitations or uncertainty, mention them transparently.
- End with a short Sources section using the evidence provided.
"""
                )
            ]
        )

    
    # Main compose method (LCEL-safe)
    
    def compose(
        self,
        query: str,
        documents: List[Document],
        fact_check_result: Dict
    ) -> str:
        """
        Generate a final, user-facing response grounded
        strictly in retrieved documents.
        """

        analysis = fact_check_result.get("analysis", "")
        formatted_sources = self._extract_sources(documents)

        response = (self.prompt | self.llm).invoke(
            {
                "query": query,
                "analysis": analysis,
                "sources": formatted_sources
            }
        )

        return response.content

    
    # Source extraction (precise & citation-safe)
    
    @staticmethod
    def _extract_sources(documents: List[Document]) -> str:
        if not documents:
            return "No sources available."

        seen = set()
        lines = []

        for d in documents:
            meta = d.metadata or {}

            doc_type = meta.get("document_type", "unknown")
            source = meta.get("source", "unknown")

            if "page" in meta:
                location = f"page {meta['page']}"
            elif "section" in meta:
                location = f"section: {meta['section']}"
            else:
                location = "location: unknown"

            key = (doc_type, source, location)
            if key in seen:
                continue

            seen.add(key)
            lines.append(f"- {doc_type} | {source} | {location}")

        return "\n".join(lines)
