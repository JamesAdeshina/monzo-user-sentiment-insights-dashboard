#%%
# ------------------------------------------------------------
# 1. Setup & Imports
# ------------------------------------------------------------
"""
Notebook: 03_data_model_preparation.ipynb
Author: James O. Adeshina
Date: October 2025

Objective:
----------
Prepare the Monzo Sentiment dataset for analytical modeling by:
- Engineering new features
- Creating dimensional tables
- Exporting BigQuery-ready schemas
"""

import pandas as pd
import numpy as np
import os


#%%

# === Paths ===
DATA_PATH = "../data/processed/Monzo_Sentiment_Scored.csv"
WAREHOUSE_PATH = "../data/warehouse/"
os.makedirs(WAREHOUSE_PATH, exist_ok=True)

# === Load dataset ===
print("📂 Loading sentiment-scored dataset...")
monzo_df = pd.read_csv(DATA_PATH)
print(f"✅ Loaded {len(monzo_df):,} rows and {monzo_df.shape[1]} columns.")
monzo_df.head(3)
#%%
# ------------------------------------------------------------
# 2. Feature Engineering
# ------------------------------------------------------------

print("🧠 Engineering new analytical features...")

# Review length (in characters)
monzo_df["review_length"] = monzo_df["review_text"].astype(str).str.len()

# Flag developer replies
monzo_df["has_reply"] = monzo_df["developer_reply_text"].notna().astype(int)

# Rating category for easier analysis
def rating_category(r):
    if r >= 4: return "High"
    elif r == 3: return "Medium"
    else: return "Low"

monzo_df["rating_category"] = monzo_df["rating"].apply(rating_category)

# Review date parsing
monzo_df["review_date"] = pd.to_datetime(monzo_df["review_date"], errors="coerce", utc=True)
monzo_df["review_year"] = monzo_df["review_date"].dt.year
monzo_df["review_month"] = monzo_df["review_date"].dt.month
monzo_df["review_week"] = monzo_df["review_date"].dt.isocalendar().week

print("✅ Feature engineering complete.")
monzo_df[["rating", "rating_category", "review_length", "has_reply"]].head(3)

#%%
# Summary of engineered features
summary = {
    "Total Reviews": len(monzo_df),
    "Missing Review Text": monzo_df["review_text"].isna().sum(),
    "Avg. Review Length": monzo_df["review_length"].mean(),
    "Reviews with Developer Reply": monzo_df["has_reply"].sum(),
    "Rating Category Counts": monzo_df["rating_category"].value_counts().to_dict(),
    "Years Covered": monzo_df["review_year"].dropna().unique().tolist()
}

from pprint import pprint
pprint(summary)

#%%
# ------------------------------------------------------------
# 3. Dimensional Tables
# ------------------------------------------------------------

print("🧩 Creating dimension tables...")

# Platform dimension
dim_platform = monzo_df[["platform"]].drop_duplicates().reset_index(drop=True)
dim_platform["platform_id"] = dim_platform.index + 1

# Version dimension
dim_version = monzo_df[["app_version"]].drop_duplicates().reset_index(drop=True)
dim_version["version_id"] = dim_version.index + 1

# Date dimension
dim_date = monzo_df[["review_date", "review_year", "review_month", "review_week"]].drop_duplicates()
dim_date = dim_date.sort_values("review_date").reset_index(drop=True)
dim_date["date_id"] = dim_date.index + 1

# Sentiment dimension
dim_sentiment = (
    monzo_df[["sentiment_label"]]
    .drop_duplicates()
    .reset_index(drop=True)
)
dim_sentiment["sentiment_id"] = dim_sentiment.index + 1

print("✅ Dimensions created:")
print(f"   - Platform: {len(dim_platform)}")
print(f"   - Version: {len(dim_version)}")
print(f"   - Date: {len(dim_date)}")
print(f"   - Sentiment: {len(dim_sentiment)}")

#%%
# ------------------------------------------------------------
# 4. FactReviews Table
# ------------------------------------------------------------

print("🧮 Building FactReviews table...")

fact_reviews = monzo_df.copy()

# Merge ID references from dimensions
fact_reviews = fact_reviews.merge(dim_platform, on="platform", how="left")
fact_reviews = fact_reviews.merge(dim_version, on="app_version", how="left")
fact_reviews = fact_reviews.merge(dim_date, on="review_date", how="left")
fact_reviews = fact_reviews.merge(dim_sentiment, on="sentiment_label", how="left")

# Select key columns
fact_reviews = fact_reviews[[
    "review_date", "rating", "rating_category",
    "review_text", "review_length",
    "has_reply", "sentiment_score", "sentiment_label",
    "platform_id", "version_id", "date_id", "sentiment_id"
]]

print(f"✅ FactReviews shape: {fact_reviews.shape}")
fact_reviews.head(3)

#%%
# ------------------------------------------------------------
# 5. Export Dimensional & Fact Tables
# ------------------------------------------------------------

print("💾 Exporting all warehouse tables...")

fact_reviews.to_csv(os.path.join(WAREHOUSE_PATH, "FactReviews.csv"), index=False)
dim_platform.to_csv(os.path.join(WAREHOUSE_PATH, "DimPlatform.csv"), index=False)
dim_version.to_csv(os.path.join(WAREHOUSE_PATH, "DimVersion.csv"), index=False)
dim_date.to_csv(os.path.join(WAREHOUSE_PATH, "DimDate.csv"), index=False)
dim_sentiment.to_csv(os.path.join(WAREHOUSE_PATH, "DimSentiment.csv"), index=False)

print("✅ All warehouse tables exported successfully.")
print(f"📁 Location: {WAREHOUSE_PATH}")
#%%
import pandas as pd
import os

DATA_DIR = "../data/warehouse"
SAFE_DIR = "../data/warehouse_safe"
os.makedirs(SAFE_DIR, exist_ok=True)

for file in os.listdir(DATA_DIR):
    if file.endswith(".csv"):
        path_in = os.path.join(DATA_DIR, file)
        path_out = os.path.join(SAFE_DIR, file)

        df = pd.read_csv(path_in)
        df.to_csv(
            path_out,
            index=False,
            quoting=1,            # csv.QUOTE_ALL
            escapechar="\\",      # escape problematic quotes
            encoding="utf-8"
        )
        print(f"✅ Re-exported safely: {path_out}")

#%%

#%%

#%%
