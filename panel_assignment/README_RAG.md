# Retrieval-Augmented Generation (RAG) Panel Assignment Pipeline - Overview

This is an overview of machine learning pipeline for predicting academic panel assignments using RAG

## 1. Data Collection & Cleaning

### a. Scrape Lecturer Data
- **`src/WebScrapping/ScholarURL.py`**  
  Scrapes UTM academic staff info and UTM Scholar URLs.  
  **Output:** `data/raw/utm_lecturers_scholarURL.xlsx`

### b. Scrape Panel Publications & Grants
- **`src/WebScrapping/LectPubGrantt.py`**  
  Uses Selenium to extract publication and grant titles for each lecturer from UTM Scholar.  
  **Output:** `data/interim/panel-publications-grants-complete-row.xlsx`

### c. Remove Empty Titles
- **`notebook_RAG/1removeEmptyColumn.ipynb`**  
  Cleans publication/grant data by removing rows with empty titles.  
  **Output:** `data/processed/panel-publications-grants-complete-row-cleaned.xlsx`

### d. Merge Panel & Project Data
- **`merge_RAG_data.py`**  
  Merges project and examiner data using `src/data/mergerRAG.py`.  
  **Output:** `data/interim/merged_panel_project_title_area.xlsx`

- **`src/data/mergerRAG.py`**  
  Contains the function to merge project and panel assignment data.

### e. Combine All Data
- **`notebook_RAG/2appendFile.ipynb`**  
  Appends cleaned publication/grant data to merged panel/project data.  
  **Output:** `data/processed/combined-project-panel.xlsx`

---

## 2. Embedding & Vector Store

### a. Save Embeddings
- **`src/LangChain/saveEmbedding.ipynb`**  
  Loads combined data, creates LangChain `Document` objects, generates embeddings, and saves to FAISS vector DB.  
  **Output:** `panel_db/` (FAISS index)

---

## 3. Retrieval-Augmented Recommendation

### a. RAG Flow & Testing
- **`src/LangChain/RAGflow.ipynb`**  
  Loads FAISS DB, defines retrieval and recommendation functions, and tests with sample queries.

- **`src/LangChain/RAGflow.py`**  
  Contains main functions:
  - `match_student_to_panel`: Retrieves similar panels for a given project.
  - `query_groq_for_panel_selection`: Formats context and queries Groq LLM for recommendations.

---

## 4. Telegram Bot (Optional)

- **`src/LangChain/RAG_Telegram.ipynb`**  
  Integrates the RAG flow with Telegram, allowing users to get recommendations via chat.

---

## Summary Table

| Step                | File/Notebook                                      | Output/Functionality                                      |
|---------------------|----------------------------------------------------|-----------------------------------------------------------|
| Scrape lecturers    | `ScholarURL.py`                                    | Raw lecturer info & Scholar URLs                          |
| Scrape publications | `LectPubGrantt.py`                                 | Raw publication/grant titles                              |
| Clean data          | `1removeEmptyColumn.ipynb`                         | Cleaned publication/grant data                            |
| Merge panel/project | `merge_RAG_data.py`, `mergerRAG.py`                | Merged panel/project assignments                          |
| Combine all         | `2appendFile.ipynb`                                | Final combined dataset                                    |
| Save embeddings     | `saveEmbedding.ipynb`                              | FAISS vector DB                                           |
| RAG flow            | `RAGflow.py`, `RAGflow.ipynb`                      | Retrieval & recommendation functions                      |
| Telegram bot        | `RAG_Telegram.ipynb`                               | Chat-based recommendations                                |

---

## Usage

1. Run each file/notebook in order as above.
2. Use `match_student_to_panel` for recommendations.
3. (Optional) Deploy Telegram bot for interactive access.

---