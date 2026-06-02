import os
import pandas as pd
from bs4 import BeautifulSoup

def clean_text(text):
    """
    Helper function to normalize text data, remove HTML tags, and convert to lowercase.
    """
    if pd.isna(text):
        return text
    text = str(text).strip().lower()
    text = BeautifulSoup(text, "lxml").get_text()
    text = text.replace('\n', ' ').replace('\t', ' ').replace('  ', ' ')
    return text

def process_and_clean_data(input_path="data/raw/Anime_top_10000.csv", output_path="data/processed/Anime_top_10000_clean.csv"):
    """
    Loads raw CSV, performs types conversion, removes statistical outliers, 
    and engineers new duration features.
    """
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Raw data file not found at {input_path}")
        
    df = pd.read_csv(input_path)
    df_clean = df.copy()

    print("--> Starting data cleaning and feature engineering...")

    # 1. Standardize string fields
    df_clean['Title'] = df_clean['Title'].apply(clean_text)

    # 2. Convert and impute numerical features
    df_clean['Score'] = pd.to_numeric(df_clean['Score'], errors='coerce')
    df_clean['Score'] = df_clean['Score'].fillna(df_clean['Score'].mean())

    if df_clean['Members'].dtype == 'object':
        df_clean['Members'] = df_clean['Members'].str.replace(',', '').str.replace(' members', '')
    df_clean['Members'] = pd.to_numeric(df_clean['Members'], errors='coerce').fillna(0)

    df_clean['Episodes'] = pd.to_numeric(df_clean['Episodes'], errors='coerce').fillna(12)

    # 3. Filter popularity outliers using Interquartile Range (IQR) rule
    q1 = df_clean['Members'].quantile(0.25)
    q3 = df_clean['Members'].quantile(0.75)
    iqr = q3 - q1
    df_clean = df_clean[(df_clean['Members'] >= q1 - 1.5 * iqr) & (df_clean['Members'] <= q3 + 1.5 * iqr)].copy()

    # 4. Handle Datetime conversions safely
    df_clean['Start_Date'] = pd.to_datetime(df_clean['Start_Date'], errors='coerce')
    df_clean['End_Date'] = pd.to_datetime(df_clean['End_Date'], errors='coerce')

    # Impute missing or ongoing dates with today's date
    today = pd.Timestamp.today()
    df_clean['Start_Date'] = df_clean['Start_Date'].fillna(today)
    df_clean['End_Date'] = df_clean['End_Date'].fillna(today)

    # 5. Feature Engineering: Calculate total duration in months
    df_clean['Duration_months'] = (
        (df_clean['End_Date'].dt.year - df_clean['Start_Date'].dt.year) * 12 +
        (df_clean['End_Date'].dt.month - df_clean['Start_Date'].dt.month)
    )
    df_clean['Duration_months'] = df_clean['Duration_months'].clip(lower=0)

    # 6. Feature Engineering: Discretize anime scores into semantic groups
    df_clean['Score_group'] = pd.cut(
        df_clean['Score'],
        bins=[0, 7, 8, 9, 10],
        labels=['Low', 'Medium', 'High', 'Top']
    )

    # Save processed data
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df_clean.to_csv(output_path, index=False, encoding="utf-8-sig")
    print(f"--> Cleaned dataset successfully saved to {output_path}. Total rows: {len(df_clean)}")
    return output_path
