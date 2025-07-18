import pandas as pd
from src.data.mergerRAG import merge_panel_and_project_data

# Load data from Excel
project_df = pd.read_excel("data/raw/project_data.xlsx")
panel_df = pd.read_excel("data/raw/examiner_data.xlsx")

# Merge and transform
merged_df = merge_panel_and_project_data(project_df, panel_df)

# Save output
merged_df.to_excel("data/interim/merged_panel_project_title_area.xlsx", index=False)
