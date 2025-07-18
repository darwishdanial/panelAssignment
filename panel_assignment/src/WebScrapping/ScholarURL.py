from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import pandas as pd
import time
import re

# Set up headless Chrome browser
options = Options()
options.add_argument("--headless=new")
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

# Define URLs and roles
urls = {
    "Professor": "https://comp.utm.my/academic-staff-professor/",
    "Associate Professor": "https://comp.utm.my/academic-staff-associate-professor/",
    "Senior Lecturer": "https://comp.utm.my/academic-staff-senior-lecturer/",
    "Lecturer": "https://comp.utm.my/academic-staff-lecturer/"
}

# Regex pattern to remove titles
title_pattern = re.compile(
    r'\b(?:Prof\.?|Assoc\.?|Dr\.?|Ts\.?|@.*?)\b', flags=re.IGNORECASE
)

def clean_name(name):
    # Remove academic titles
    title_pattern = re.compile(r'\b(?:Prof\.?|Assoc\.?|Dr\.?|Ts\.?|@.*?)\b', flags=re.IGNORECASE)
    cleaned = title_pattern.sub('', name)

    # Remove leading dots, non-breaking spaces, and extra whitespace
    cleaned = re.sub(r'^(\.|·|\s| )+', '', cleaned)  # handles `...` or `·` or spaces
    return ' '.join(cleaned.split())  # normalise internal spacing

all_lecturers = []

for role, url in urls.items():
    print(f"Scraping {role}...")
    driver.get(url)
    time.sleep(3)

    soup = BeautifulSoup(driver.page_source, "html.parser")
    lecturer_blocks = soup.find_all("div", class_="elementor-widget-wrap")

    for block in lecturer_blocks:
        # Extract raw name
        name_tag = block.find("h5", class_="elementor-image-box-title")
        raw_name = name_tag.get_text(strip=True) if name_tag else None
        name = clean_name(raw_name) if raw_name else None

        # Extract email
        email_tag = block.find("i")
        email = email_tag.get_text(strip=True) if email_tag else None

        # Extract UTM Scholar link and ID
        scholar_link_tag = block.find("a", href=lambda href: href and "utmscholar.utm.my/Scholar/ScholarInfoDetails/" in href)
        scholar_url = scholar_link_tag['href'] if scholar_link_tag else None
        scholar_id = scholar_url.split("/")[-1] if scholar_url else None

        if name:
            all_lecturers.append({
                "lecturer_name": name,
                "email": email,
                "role": role,
                "scholar_url": scholar_url,
                "scholar_id": scholar_id
            })

driver.quit()

# Convert to DataFrame and export
df = pd.DataFrame(all_lecturers)
output_path = r"C:\Users\adarw\OneDrive\Documents\fypagile\panelAssignment\panel_assignment\data\raw\utm_lecturers_scholarURL.xlsx"
df.to_excel(output_path, index=False)

print(f"\n✅ Done. Scraped {len(all_lecturers)} lecturers.")
print(f"📄 Data saved to: {output_path}")
