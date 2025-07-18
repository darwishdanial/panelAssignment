import pandas as pd

def merge_panel_and_project_data(project_df: pd.DataFrame, panel_df: pd.DataFrame) -> pd.DataFrame:
    panel_grouped = panel_df.groupby("project_id").agg(list).reset_index()

    merged_rows = []

    for _, project in project_df.iterrows():
        project_id = project["project_id"]
        project_title = project.get("title", "")
        project_area = project.get("area", "")
        project_type = project.get("type", "")

        if pd.isna(project_area):
            continue

        panel_rows = panel_df[panel_df["project_id"] == project_id]

        for _, row in panel_rows.iterrows():
            merged_rows.append({
                "title": f"{project_title} ({project_area})",
                "source": "fyp panel assignment",
                "lecturer_name": row["name"]
            })

    return pd.DataFrame(merged_rows)
