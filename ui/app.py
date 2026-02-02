import sys
from pathlib import Path
import streamlit as st


# import path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(PROJECT_ROOT))

from ingestion.ingestion_pipeline import IngestionPipeline
from orchestration.lcel_pipeline import build_agentic_rag_chain


# Page Config

st.set_page_config(
    page_title="Agentic RAG Academic Validation",
    page_icon=" ",
    layout="wide"
)

st.title("EvidenceGPT")
st.caption("Multi-Agent RAG Validator : View knowledge through verified sources")


# Session State (CRITICAL)

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "index_ready" not in st.session_state:
    st.session_state.index_ready = False

if "agentic_rag_chain" not in st.session_state:
    st.session_state.agentic_rag_chain = None


# Sidebar: File Upload

st.sidebar.header("📂 Upload Research Files")

uploaded_files = st.sidebar.file_uploader(
    "Upload files (PDF, DOCX, PPTX, XLSX, TXT)",
    type=["pdf", "docx", "pptx", "xlsx", "txt"],
    accept_multiple_files=True
)


# Save Uploaded Files

def save_uploaded_file(uploaded_file):
    ext = uploaded_file.name.split(".")[-1].lower()

    folder_map = {
        "pdf": "pdf",
        "docx": "docx",
        "pptx": "ppts",
        "xlsx": "excels",
        "txt": "texts",
    }

    if ext not in folder_map:
        return

    save_dir = PROJECT_ROOT / "data" / folder_map[ext]
    save_dir.mkdir(parents=True, exist_ok=True)

    save_path = save_dir / uploaded_file.name
    with open(save_path, "wb") as f:
        f.write(uploaded_file.getbuffer())


# Upload Handling + Index Rebuild

if uploaded_files:
    with st.sidebar.spinner("Saving files..."):
        for file in uploaded_files:
            save_uploaded_file(file)

    st.sidebar.success("Files uploaded successfully!")

if st.sidebar.button("🔄 Rebuild Knowledge Index"):
    with st.spinner("Running ingestion pipeline..."):
        pipeline = IngestionPipeline(
            faiss_dir="vectorstore/faiss_index"
        )
        pipeline.run()

    # rebuild LCEL chain AFTER ingestion
    st.session_state.agentic_rag_chain = build_agentic_rag_chain(
        "vectorstore/faiss_index"
    )

    st.session_state.index_ready = True
    st.sidebar.success("FAISS index rebuilt successfully!")


# Display Chat History

for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])


# Chat Input

user_query = st.chat_input("Ask a question about the uploaded research data...")

if user_query:
    st.session_state.chat_history.append(
        {"role": "user", "content": user_query}
    )

    with st.chat_message("user"):
        st.markdown(user_query)

    with st.chat_message("assistant"):
        if not st.session_state.index_ready or st.session_state.agentic_rag_chain is None:
            st.warning(" Please upload files and rebuild the index first.")
        else:
            with st.spinner("🔍 Analyzing documents..."):
                result = st.session_state.agentic_rag_chain.invoke(
                    {"query": user_query}
                )

                st.markdown(result)

                st.session_state.chat_history.append(
                    {"role": "assistant", "content": result}
                )
