import os
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

def run_exploratory_analysis(input_path="data/processed/Anime_top_10000_clean.csv"):
    """
    Generates descriptive statistics and saves key analytical visualizations.
    """
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Cleaned data file not found at {input_path}")

    df_clean = pd.read_csv(input_path)
    sns.set_style("whitegrid")

    print("\n=== DESCRIPTIVE STATISTICS ===")
    print(df_clean[['Score', 'Episodes', 'Members', 'Duration_months']].describe())
    
    print("\n=== ANIME COUNT BY TYPE ===")
    print(df_clean['Type'].value_counts())

    # Create a directory to store visualizations if needed
    os.makedirs("visualizations", exist_ok=True)

    # Plot 1: Score Distribution
    plt.figure(figsize=(8, 5))
    sns.histplot(df_clean['Score'], bins=30, kde=True)
    plt.title('Anime Score Distribution')
    plt.xlabel('Score')
    plt.ylabel('Count')
    plt.savefig("visualizations/score_distribution.png", dpi=100)
    plt.close()

    # Plot 2: Score vs Members (Regression Analysis)
    plt.figure(figsize=(8, 5))
    sns.regplot(data=df_clean, x='Members', y='Score',
                scatter_kws={'alpha': 0.4, 's': 20},
                line_kws={'color': 'red'})
    plt.title('Correlation: Anime Score vs Members Volume')
    plt.xlabel('Members Count')
    plt.ylabel('Score')
    plt.savefig("visualizations/score_vs_members.png", dpi=100)
    plt.close()

    # Plot 3: Correlation Matrix Heatmap
    plt.figure(figsize=(6, 5))
    corr = df_clean[['Score', 'Episodes', 'Members', 'Duration_months']].corr()
    sns.heatmap(corr, annot=True, fmt='.2f', cmap='coolwarm', center=0)
    plt.title('Numerical Variables Correlation Matrix')
    plt.tight_layout()
    plt.savefig("visualizations/correlation_matrix.png", dpi=100)
    plt.close()

    print("--> EDA charts successfully generated and saved into 'visualizations/' directory.")