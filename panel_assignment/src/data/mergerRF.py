import pandas as pd

def get_categories():
    return {
        'Mobile Application': ['mobile application', 'mobile', 'android', 'ios', 'apps'],
        'Web Development': ['cross-platform', 'full', 'web-based', 'stack', 'web', 'html', 'css', 'javascript', 'frontend', 'backend', 'system', 'ui', 'ux', 'application development', 'app development', 'desktop application'],
        'Machine Learning': ['multi-omics', 'data analytics', 'data visualization', 'data science', 'predictive analysis', 'text mining', 'automation', 'chatbot', 'ai-powered', 'smart', 'text-mining', 'autonomous', 'speech', 'machine learning', 'ml', 'ai', 'artificial intelligence', 'processing', 'classification', 'recognition', 'prediction', 'intelligence', 'analytics', 'analysis'],
        'Security': ['penetration', 'steganography', 'identifiable', 'cyber', 'passcode', 'security', 'network security', 'encryption', 'crime', 'fraud', 'scam', 'cryptography', 'biometric'],
        'Augmented Reality': ['real-world', 'twin', 'mapping', 'metaverse', 'augmented reality', 'ar', 'vr', 'virtual reality', 'reality', 'augmented', 'virtual'],
        'Game Development': ['sdk', 'multiplayer', 'game', 'game development', 'gaming'],
        'Management': ['managing', 'timetable', 'scheduling', 'project management', 'management', 'communication', 'schedule', 'booking'],
        'Education': ['university', 'education', 'learning', 'teaching'],
        'Networking': ['telecom', 'network', 'networking', 'sdn', 'wireless mesh', 'iot', 'client server', 'embedded computing', 'internet of things', 'logistic'],
        'Health & Medical': ['sport', 'biology', 'donation', 'counseling', 'sports', 'health', 'fitness', 'wellness', 'antimicrobial', 'cancer', 'disease', 'diabetes', 'medical', 'bioinformatics', 'breast cancer', 'lung cancer', 'pneumonia detection', 'drug discovery', 'cancer drug response', 'medical data', 'hospitality'],
        'Financial & Business': ['payment', 'rental', 'buy', 'fintech', 'financial', 'stock price', 'investment', 'business', 'e-commerce', 'financial tech', 'fraud detection', 'economic', 'business - investment', 'ecommerce'],
        'Human-Computer Interaction (HCI)': ['interactive computer graphics', 'human computer interaction', 'hci', 'gesture recognition', 'graphics design', 'usability'],
        'Computer Vision': ['computer vision', 'object detection', 'facial detection', 'image denoising', 'real-time computer graphics', 'image filtering', 'realtime computer graphics'],
        'Social & Tourism': ['social', 'tourism', 'accommodation', 'online drivers', 'public transportation', 'travel', 'tourism planning'],
        'UTM': ['utm', 'multimedia and hci'],
        'Others': []
    }

def match_category(project_area: str) -> str:
    area = ' '.join(project_area.lower().split())
    for category, keywords in get_categories().items():
        for keyword in keywords:
            if keyword in area:
                return category
    return 'Others'

def merge_panel_and_project_data(project_df: pd.DataFrame, panel_df: pd.DataFrame) -> pd.DataFrame:
    panel_grouped = panel_df.groupby("project_id").agg(list).reset_index()

    merged_rows = []

    for _, project in project_df.iterrows():
        project_id = project["project_id"]
        project_area = project.get("area", "")
        project_type = project.get("type", "")

        if pd.isna(project_area):
            continue

        matched_category = match_category(project_area)
        panel_rows = panel_df[panel_df["project_id"] == project_id]

        for _, row in panel_rows.iterrows():
            merged_rows.append({
                "project_area": matched_category,
                "project_type": project_type,
                "lecturer_name": row["name"]
            })

    return pd.DataFrame(merged_rows)
