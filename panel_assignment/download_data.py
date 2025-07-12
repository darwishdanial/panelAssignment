# download_data.py

from src.data.loader import fetch_and_save_json

# URLs
project_url = "http://web.fc.utm.my/~wmf12apps2/cgi-bin/webman/psm2/index_json-v2.cgi?entity=project"
examiner_url = "http://web.fc.utm.my/~wmf12apps2/cgi-bin/webman/psm2/index_json-v2.cgi?entity=examiner"

# Output files
project_output = "data/raw/project_data.xlsx"
examiner_output = "data/raw/examiner_data.xlsx"

# Run
fetch_and_save_json(project_url, project_output)
fetch_and_save_json(examiner_url, examiner_output)
