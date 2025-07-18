import pandas as pd
import time
import random
import re
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from tqdm import tqdm

# === Helper: Clean illegal Excel characters ===
def clean_excel_string(s):
    if isinstance(s, str):
        s = re.sub(r'[\x00-\x1F]+', ' ', s)  # Remove control characters
    return s

# === Load Excel file ===
input_file = "../../data/interim/filled-scholar.xlsx"
df = pd.read_excel(input_file)

# === Set up Selenium WebDriver ===
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

# === Output paths ===
output_path_partial = "../../data/raw/panel-publications-grants-partial-row.xlsx"
output_path_final = "../../data/interim/panel-publications-grants-complete-row.xlsx"

results = []

# === Extract publication titles ===
def extract_publications(soup):
    publications = []
    pub_table = soup.find("table", {"id": "publicationListTablePersonalDatatable"})
    if pub_table:
        rows = pub_table.find("tbody").find_all("tr")
        for r in rows:
            a = r.find("a")
            if a:
                publications.append(a.get_text(strip=True))
    return publications

# === Extract grant titles ===
def extract_grants(soup):
    grants = []
    rows = soup.select("#grantListTablePersonalDatatable tbody tr")
    for row in rows:
        td = row.select_one("td")
        if td:
            raw_html = str(td)
            if '<br' in raw_html:
                title_html = raw_html.split('<br')[0]
                title_text = BeautifulSoup(title_html, 'html.parser').get_text(strip=True)
                grants.append(title_text)
            else:
                grants.append(td.get_text(strip=True))
    return grants

# === Start scraping loop ===
for i, row in tqdm(df.iterrows(), total=len(df), desc="Scraping UTM Scholar"):
    name = row["lecturer_name"]
    url = row["scholar_url"]

    try:
        driver.get(url)
        time.sleep(random.uniform(18, 22))
        soup = BeautifulSoup(driver.page_source, "html.parser")

        pub_titles = extract_publications(soup)
        grant_titles = extract_grants(soup)

        if pub_titles:
            for title in pub_titles:
                results.append({
                    "title": title,
                    "source": "publication",
                    "lecturer_name": name
                })

        if grant_titles:
            for title in grant_titles:
                results.append({
                    "title": title,
                    "source": "grant",
                    "lecturer_name": name
                })

    except Exception as e:
        results.append({
            "title": f"Error: {str(e)}",
            "source": "error",
            "lecturer_name": name,
        })

    # Save partial every 10 lecturers
    if (i + 1) % 10 == 0:
        df_partial = pd.DataFrame(results).applymap(clean_excel_string)
        df_partial.to_excel(output_path_partial, index=False)
        print("✅ Added", i + 1,"[",name,"]" "panels. Partial saved to:", output_path_partial)

# === Final Save ===
driver.quit()
df_final = pd.DataFrame(results).applymap(clean_excel_string)
df_final.to_excel(output_path_final, index=False)

print("✅ Scraping complete. Final results saved to:", output_path_final)
