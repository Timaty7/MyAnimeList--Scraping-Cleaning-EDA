import os
import sys

# Crucial Senior Fix: Automatically add the current project directory to the Python path.
# This prevents 'ModuleNotFoundError' when running from different environments.
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

# Now it is completely safe to import internal packages
from src.scraper import scrape_top_anime
from src.cleaner import process_and_clean_data
from src.eda import run_exploratory_analysis

def main():
    raw_data_path = "data/raw/Anime_top_10000.csv"
    processed_data_path = "data/processed/Anime_top_10000_clean.csv"

    print("==================================================")
    print("🚀 PIPELINE INITIALIZATION: MYANIMELIST DATA WORKFLOW")
    print("==================================================")

    # Step 1: Check if raw data exists, if not -> trigger web scraping
    if not os.path.exists(raw_data_path):
        print(f"[INFO] Raw data target '{raw_data_path}' not found.")
        # Scraping full 10000 rows. Change limit_end=100 for a quick safety test run.
        scrape_top_anime(limit_start=0, limit_end=10000, step=50, output_path=raw_data_path)
    else:
        print(f"[INFO] Existing raw data asset discovered at '{raw_data_path}'. Proceeding...")

    # Step 2: Run Data Processing & Feature Engineering Pipeline
    try:
        process_and_clean_data(input_path=raw_data_path, output_path=processed_data_path)
    except Exception as e:
        print(f"[CRITICAL ERROR] Data cleaning stage failed: {e}")
        return

    # Step 3: Run Exploratory Data Analysis & Visualizations
    try:
        run_exploratory_analysis(input_path=processed_data_path)
    except Exception as e:
        print(f"[CRITICAL ERROR] EDA visualization stage failed: {e}")
        return

    print("==================================================")
    print("✅ PIPELINE EXECUTION SUCCESSFUL: ALL ASSETS READY")
    print("==================================================")

if __name__ == "__main__":
    main()