from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings

def load_faiss_index(path: str):
    embeddings = OpenAIEmbeddings()
    return FAISS.load_local(
        path,
        embeddings,
        allow_dangerous_deserialization=True
    )
