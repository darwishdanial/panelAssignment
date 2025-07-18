from collections import defaultdict
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
from groq import Groq  # Make sure groq SDK is installed: pip install groq
from dotenv import load_dotenv
import os

load_dotenv()  # Load variables from .env
api_key = os.getenv("GROQ_API_KEY")

# =========================
# 🔧 Setup: Embeddings & Vector DB
# =========================

embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
db = FAISS.load_local("panel_db", embeddings=embedding_model, allow_dangerous_deserialization=True)

# =========================
# 🔧 Setup: Groq API
# =========================

client = Groq(api_key=api_key)  # Replace with your key

def query_groq_for_panel_selection(panel_matches: dict, student_title: str, student_area: str) -> str:
    # Format context for LLM
    context = f"Student Project Title: {student_title}\nStudent Project Area: {student_area}\n\n"
    context += "Relevant Panel Data:\n"

    for panel, items in panel_matches.items():
        context += f"\nPanel {panel}:\n"
        for item in items:
            context += f"- {item}\n"

    # Prompt
    prompt = f"""
You are an academic panel recommender system. Based on the student’s title and project area, and the matching history (publication, grants, assignments) of each panel, recommend the top 5 most suitable panels and give a short reason for each.

{context}

Return the result in this format:

1. Panel X - Reason
2. Panel Y - Reason
...
"""

    # Query Groq LLM
    response = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[
            {"role": "system", "content": "You are an intelligent assistant that recommends academic panels based on expertise."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.4
    )

    return response.choices[0].message.content

# =========================
# 🔁 Main Flow Function
# =========================

def match_student_to_panel(student_title: str, student_area: str) -> str:
    query_text = f"{student_title} - {student_area}"
    query_embedding = embedding_model.embed_query(query_text)

    # Search top 10 most similar docs
    retrieved_docs = db.similarity_search_by_vector(query_embedding, k=10)

    # Group matched documents by panel
    panel_matches = defaultdict(list)
    for doc in retrieved_docs:
        panel = doc.metadata["lecturer_name"]
        source = doc.metadata["source"]
        panel_matches[panel].append(f"[{source.upper()}] {doc.page_content}")

    # Get recommendations from Groq
    result = query_groq_for_panel_selection(panel_matches, student_title, student_area)
    return result

student_title = "Enhancing Medical Imaging using GANs"
student_area = "Deep Learning in Healthcare"

recommendation = match_student_to_panel(student_title, student_area)
print(recommendation)