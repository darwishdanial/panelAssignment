# download_data.py
from dotenv import load_dotenv
import os

load_dotenv()  # Load variables from .env
PROJECT_URL = os.getenv("PROJECT_URL")
EXAMINER_URL = os.getenv("EXAMINER_URL")

from src.data.loader import fetch_and_save_json

# URLs
project_url = PROJECT_URL
examiner_url = EXAMINER_URL

# Output files
project_output = "data/raw/project_data.xlsx"
examiner_output = "data/raw/examiner_data.xlsx"

# Run
fetch_and_save_json(project_url, project_output)
fetch_and_save_json(examiner_url, examiner_output)
