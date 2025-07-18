import pandas as pd
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.docstore.document import Document

# ✅ Step 1: Read Excel
df = pd.read_excel("../../data/processed/combined-project-panel.xlsx")

# Optional: clean & validate
df = df.dropna(subset=["lecturer_name", "title", "source"])
df["lecturer_name"] = df["lecturer_name"].str.strip()
df["title"] = df["title"].str.strip()
df["source"] = df["source"].str.strip()

# ✅ Step 2: Prepare LangChain Documents
docs = []
for _, row in df.iterrows():
    doc = Document(
        page_content=row["title"],
        metadata={
            "lecturer_name": row["lecturer_name"],
            "source": row["source"]
        }
    )
    docs.append(doc)

# ✅ Step 3: Generate Embeddings & Save to FAISS
embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2", device="cpu")
db = FAISS.from_documents(docs, embedding_model)
db.save_local("panel_db")  # This creates panel_db/index.faiss and panel_db/index.pkl
