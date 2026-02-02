from typing import Dict, List


class DocumentRoutingAgent:
    """
    Decides which document types should be searched
    based on the classified query intent.

    This agent is RULE-FIRST (deterministic) and
    production-safe for academic RAG systems.
    """

    
    # Canonical document types used across the system
   
    ALL_DOC_TYPES = ["pdf", "docx", "pptx", "xlsx", "txt"]

   
    # Query-type → document routing rules
    
    ROUTING_RULES: Dict[str, List[str]] = {
        # Academic / research questions
        "research": ["pdf", "docx", "pptx"],

        # Conceptual explanations, theory
        "conceptual": ["pdf", "docx", "txt", "pptx"],

        # Resume / profile / skills queries
        "profile": ["docx", "pdf"],

        # Numerical / tabular questions
        "data": ["xlsx", "csv"],

        # Presentation-style summaries
        "presentation": ["pptx", "pdf"],

        # General QA fallback
        "general": ALL_DOC_TYPES,
    }

    def route(self, query_type: str) -> List[str]:
        """
        Returns a list of allowed document types
        for retrieval based on query classification.
        """

        if not query_type:
            return self.ALL_DOC_TYPES

        query_type = query_type.lower().strip()

        allowed = self.ROUTING_RULES.get(query_type)

        # Safety fallback (never return empty)
        if not allowed:
            return self.ALL_DOC_TYPES

        return allowed
