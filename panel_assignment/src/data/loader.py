# loader.py
import requests
import pandas as pd
import os

def fetch_and_save_json(url: str, output_path: str) -> None:
    """
    Fetch JSON from the given URL and save it as an Excel file.
    Handles both raw list responses and wrapped responses with a 'list' key.
    """
    print(f"Fetching from: {url}")
    response = requests.get(url)
    response.raise_for_status()

    data = response.json()

    # Handle cases where JSON is { "list": [...] }
    if isinstance(data, dict) and "list" in data:
        data_list = data["list"]
    elif isinstance(data, list):
        data_list = data
    else:
        raise ValueError("Unexpected JSON format: expected a list or a 'list' key")

    df = pd.DataFrame(data_list)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_excel(output_path, index=False)
    print(f"Saved to: {output_path}")
#test