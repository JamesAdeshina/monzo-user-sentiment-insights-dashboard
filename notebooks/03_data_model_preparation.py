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

# UX Sentiment Level dimension
dim_ux = (
    monzo_df[["ux_sentiment_level"]]
    .drop_duplicates()
    .reset_index(drop=True)
)
dim_ux["ux_id"] = dim_ux.index + 1

print(f"   - UX Sentiment Level: {len(dim_ux)}")


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

# 🩹 FIX: Safely join DimUX — avoid many-to-many explosion
# If multiple rows per sentiment level exist, keep only one representative row
dim_ux_deduped = dim_ux.drop_duplicates(subset=["ux_sentiment_level"])[["ux_sentiment_level", "ux_id"]]

fact_reviews = fact_reviews.merge(dim_ux_deduped, on="ux_sentiment_level", how="left")

# List of potential columns to include
candidate_columns = [
    "review_date", "rating", "rating_category", "review_text",
    "review_length", "has_reply", "sentiment_score", "sentiment_label",
    "csat_approx", "ces_approx", "task_success_inferred",
    "ux_health_score", "ux_sentiment_level", "ux_pain_point_flag",
    "is_pseudonymized", "platform_id", "version_id", "date_id",
    "sentiment_id", "ux_id"  # include ux_id FK now
]

# Keep only columns that exist in the dataframe
existing_columns = [col for col in candidate_columns if col in fact_reviews.columns]

# Select only valid ones
fact_reviews = fact_reviews[existing_columns]

print(f"✅ FactReviews shape: {fact_reviews.shape}")
display(fact_reviews.head(3))

#%%
from IPython.display import display

print("Dim Shapes")

display(fact_reviews.head(3))
display(dim_platform.head(3))
display(dim_version.head(3))
display(dim_date.head(3))
display(dim_sentiment.head(3))
display(dim_ux.head(3))

#%%
from IPython.display import display

# Assuming you have already loaded these DataFrames: fact_reviews, dim_platform, etc.
print("Dim Shapes")

# Display row counts and first three rows for each DataFrame
print(f"fact_reviews: {fact_reviews.shape[0]} rows")
display(fact_reviews.head(12))

print(f"dim_platform: {dim_platform.shape[0]} rows")
display(dim_platform.head(3))

print(f"dim_version: {dim_version.shape[0]} rows")
display(dim_version.head(3))

print(f"dim_date: {dim_date.shape[0]} rows")
display(dim_date.head(3))

print(f"dim_sentiment: {dim_sentiment.shape[0]} rows")
display(dim_sentiment.head(3))

print(f"dim_ux: {dim_ux.shape[0]} rows")
display(dim_ux.head(3))

#%%
dim_ux = monzo_df[[
    "ux_usability_sentiment",
    "ux_navigation_sentiment",
    "ux_performance_sentiment",
    "ux_accessibility_sentiment",
    "ux_emotional_sentiment",
    "ux_health_score",
    "ux_pain_point_flag",
    "ux_sentiment_level"
]].drop_duplicates().reset_index(drop=True)

dim_ux["ux_id"] = dim_ux.index + 1

#%%
# fact_reviews = fact_reviews.merge(dim_ux, on="ux_sentiment_level", how="left")

#%%
print(f"✅ Loaded {len(fact_reviews):,} rows and {fact_reviews.shape[1]} columns.")
#%%
# ------------------------------------------------------------
# Derive dominant UX category for each review
# ------------------------------------------------------------

def infer_ux_category(row):
    scores = {
        "usability": row.get("ux_usability_sentiment", None),
        "navigation": row.get("ux_navigation_sentiment", None),
        "performance": row.get("ux_performance_sentiment", None),
        "accessibility": row.get("ux_accessibility_sentiment", None),
        "emotional": row.get("ux_emotional_sentiment", None),
    }
    # Drop NaNs and find max
    valid_scores = {k: v for k, v in scores.items() if pd.notna(v)}
    if not valid_scores:
        return None
    return max(valid_scores, key=valid_scores.get)

fact_reviews["ux_category"] = fact_reviews.apply(infer_ux_category, axis=1)

#%%
fact_reviews["ux_category"].value_counts(dropna=False)

#%%

#%%
# from IPython.display import display
#
# print("Dim Shapes")
#
# display(fact_reviews.head(3))
# display(dim_platform.head(3))
# display(dim_version.head(3))
# display(dim_date.head(3))
# display(dim_sentiment.head(3))
# display(dim_ux.head(3))

#%%
# # ------------------------------------------------------------
# # 5. Export Dimensional & Fact Tables
# # ------------------------------------------------------------
#
# import os
# import pandas as pd
#
# # --- Setup paths ---
# FORMATS = ["csv", "gzip", "parquet"]
# for fmt in FORMATS:
#     os.makedirs(os.path.join(WAREHOUSE_PATH, fmt), exist_ok=True)
#
# # --- Tables to export ---
# tables = {
#     "FactReviews": fact_reviews,
#     "DimPlatform": dim_platform,
#     "DimVersion": dim_version,
#     "DimDate": dim_date,
#     "DimSentiment": dim_sentiment,
#     "DimUX": dim_ux
# }
#
# # --- Export loop ---
# print("💾 Exporting all warehouse tables in CSV, GZIP, and Parquet formats...")
#
# for name, table in tables.items():
#     print(f"\n📦 Exporting {name} ({table.shape[0]} rows, {table.shape[1]} cols)...")
#
#     # 1️⃣ CSV
#     csv_path = os.path.join(WAREHOUSE_PATH, "csv", f"{name}.csv")
#     table.to_csv(csv_path, index=False, encoding="utf-8")
#
#     # 2️⃣ GZIP
#     gzip_path = os.path.join(WAREHOUSE_PATH, "gzip", f"{name}.csv.gz")
#     table.to_csv(gzip_path, index=False, compression="gzip", encoding="utf-8")
#
#     # 3️⃣ Parquet
#     parquet_path = os.path.join(WAREHOUSE_PATH, "parquet", f"{name}.parquet")
#     table.to_parquet(parquet_path, index=False, compression="snappy")
#
#     # Size check
#     size_csv = os.path.getsize(csv_path) / (1024**3)
#     size_gz = os.path.getsize(gzip_path) / (1024**3)
#     size_pq = os.path.getsize(parquet_path) / (1024**3)
#
#     print(f"   • CSV:   {size_csv:.2f} GB")
#     print(f"   • GZIP:  {size_gz:.2f} GB")
#     print(f"   • PARQ:  {size_pq:.2f} GB")
#
# print("\n✅ All export formats generated successfully.")
# print(f"📁 Location: {WAREHOUSE_PATH}")

#%%
