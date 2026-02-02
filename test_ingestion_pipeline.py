from dotenv import load_dotenv
load_dotenv()

from vectorstore.faiss_loader import load_faiss_index

vs = load_faiss_index("vectorstore/faiss_index")

# HARD FILTER TEST (bypass routing)
docs = vs.similarity_search("slide", k=20)

print(" DEBUG: FAISS PPT CHECK")
for d in docs:
    print(d.metadata)
