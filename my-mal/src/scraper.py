import os
import time
import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrape_top_anime(limit_start=0, limit_end=10000, step=50, output_path="data/raw/Anime_top_10000.csv"):
    """
    Scrapes the Top Anime pages from MyAnimeList and saves the raw data to a CSV file.
    """
    # Create output directory if it does not exist
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    titles, scores, anime_types, episodes, start_dates, end_dates, members = [], [], [], [], [], [], []
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}

    print(f"--> Starting web scraping from limit={limit_start} to {limit_end}...")
    
    for limit in range(limit_start, limit_end, step):
        url = f"https://myanimelist.net/topanime.php?limit={limit}&ajax=1"
        print(f"Parsing: {url}")

        try:
            response = requests.get(url, headers=headers, timeout=15)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"[ERROR] Failed to fetch data at limit {limit}: {e}")
            print("Skipping to next page to keep the pipeline running...")
            continue

        soup = BeautifulSoup(response.text, "html.parser")
        rows = soup.find_all("tr", class_="ranking-list")

        if not rows:
            print(f"[WARNING] No rows found at limit {limit}. Breaking loop.")
            break

        for row in rows:
            # Extract Title
            title_tag = row.find("h3")
            titles.append(title_tag.text.strip() if title_tag else "N/A")

            # Extract Score
            score_tag = row.select_one("td.score span")
            scores.append(score_tag.text.strip() if score_tag else "N/A")

            # Extract Information Block
            info = row.find("div", class_="information")
            if info:
                lines = [l.strip() for l in info.text.split("\n") if l.strip()]
            else:
                lines = ["N/A", "N/A", "N/A"]

            # Parse Type and Episodes
            type_ep = lines[0] if len(lines) > 0 else "N/A"
            if "(" in type_ep:
                anime_type = type_ep.split("(")[0].strip()
                eps = type_ep.split("(")[1].replace("eps)", "").replace("ep)", "").strip()
            else:
                anime_type = type_ep
                eps = "N/A"
            anime_types.append(anime_type)
            episodes.append(eps)

            # Parse Airing Dates
            date_line = lines[1] if len(lines) > 1 else "N/A"
            date_parts = [part.strip() for part in date_line.split(" - ")]

            current_start_date = "N/A"
            current_end_date = "N/A"

            if len(date_parts) == 2:
                current_start_date = date_parts[0]
                current_end_date = date_parts[1]
            elif len(date_parts) == 1:
                current_start_date = date_parts[0]
                current_end_date = "Ongoing"

            start_dates.append(current_start_date)
            end_dates.append(current_end_date)

            # Extract Members Count
            members_line = lines[2] if len(lines) > 2 else "N/A"
            members.append(members_line)

        # Anti-bot blocking delay (Polite scraping)
        time.sleep(1)

    # Save to DataFrame and Export
    df = pd.DataFrame({
        "Title": titles,
        "Score": scores,
        "Type": anime_types,
        "Episodes": episodes,
        "Start_Date": start_dates,
        "End_Date": end_dates,
        "Members": members
    })
    
    df.to_csv(output_path, index=False, encoding="utf-8-sig")
    print(f"--> Raw dataset successfully saved. Total rows scraped: {len(df)}")
    return output_path