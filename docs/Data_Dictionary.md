# 🧾 Data Dictionary  
**Project:** Monzo User Sentiment & Feature Insights Dashboard  
**Author:** James O. Adeshina  
**Date:** October 2025  
**Version:** 1.0  

---

## 1️⃣ Purpose  
This document defines every field contained in the analytical dataset  
`Monzo_Reviews_Master` (stored as Parquet/CSV in BigQuery).  
It ensures consistent understanding across Product, UX Research, and Data teams when interpreting dashboard metrics.

---

## 2️⃣ Dataset Overview  

| Attribute | Detail |
|------------|--------|
| **Total Records** | ≈ 33 500 (app reviews from 2015 – 2025) |
| **Platforms** | Apple App Store (≈ 9 600) · Google Play Store (≈ 23 900) |
| **Granularity** | One record = one individual review |
| **Storage Location** | Google BigQuery dataset `monzo_reviews` · table `master_reviews` |
| **Primary Key** | `review_id` (derived unique hash per review text + date + platform) |

---

## 3️⃣ Field Definitions  

| Field Name | Data Type | Source | Description / Purpose |
|-------------|-----------|---------|------------------------|
| **review_id** | STRING (UUID) | Derived | Unique identifier for each review. |
| **platform** | STRING | Manual tag | `"iOS"` or `"Android"` to distinguish source store. |
| **submission_date** | DATE | Raw | Date the review was submitted (UTC). |
| **country** | STRING | Raw | Two-letter country code (e.g., `GB`, `US`). |
| **language** | STRING | Raw | ISO 639-1 language code (e.g., `en`). |
| **rating** | INTEGER (1–5) | Raw | Star rating given by user. |
| **review_title** | STRING | Raw | Headline/title of review. |
| **review_text** | STRING | Raw | Full review content (text body). |
| **review_length_words** | INTEGER | Derived | Word count of review used in EDA (length vs sentiment). |
| **review_length_chars** | INTEGER | Derived | Character count for analysis of verbosity. |
| **version_raw** | STRING | Raw | Exact app version from store metadata. |
| **version_major_minor** | STRING | Derived | Normalized to major.minor (e.g., `6.46`) for trend analysis. |
| **sentiment_score** | FLOAT (−1 → 1) | VADER NLP | Compound sentiment polarity. |
| **sentiment_label** | STRING | Derived | `Positive` ≥ 0.05 · `Neutral` between · `Negative` ≤ −0.05. |
| **theme_tags** | ARRAY<STRING> | YAKE + taxonomy | High-level Monzo features (e.g., `["Flex","Support"]`). |
| **ux_category_tags** | ARRAY<STRING> | Manual taxonomy | UX dimensions (`Usability`,`Navigation`,`Performance`,`Accessibility`,`Emotion`). |
| **developer_reply** | STRING (Nullable) | Raw | Official developer response (if present). |
| **likes** | INTEGER (Nullable) | Raw | Review up-votes (if available). |
| **dislikes** | INTEGER (Nullable) | Raw | Down-votes (if available). |
| **link** | STRING | Raw | App store review URL (reference only, not used in BI). |
| **semantic_sentiment_appfollow** | STRING | Raw | AppFollow’s proprietary sentiment label (used for cross-validation). |
| **ux_usability_sentiment** | FLOAT | Derived | Average sentiment score of reviews tagged `Usability`. |
| **ux_navigation_sentiment** | FLOAT | Derived | Average sentiment for navigation-related feedback. |
| **ux_performance_sentiment** | FLOAT | Derived | Average sentiment for speed / stability feedback. |
| **ux_accessibility_sentiment** | FLOAT | Derived | Average sentiment for accessibility mentions. |
| **ux_emotional_sentiment** | FLOAT | Derived | Sentiment around emotional response (e.g., trust, delight). |
| **nps_proxy_category** | STRING | Derived | `Promoter`, `Passive`, or `Detractor` based on sentiment score thresholds. |
| **created_at** | TIMESTAMP | System | Ingestion timestamp for ETL traceability. |

---

## 4️⃣ Dimension Tables for Power BI  

| Table Name | Key Field | Description |
|-------------|-----------|-------------|
| **DimDate** | `date_key` | Calendar attributes (year, month, week). |
| **DimPlatform** | `platform` | Platform lookup table (`iOS`,`Android`). |
| **DimVersion** | `version_major_minor` | Simplified version number for release comparison. |
| **DimTheme** | `theme_name` | List of Monzo feature themes. |
| **DimUXCategory** | `ux_category` | UX category lookup table for UX dashboard filters. |

---

## 5️⃣ Derived Metrics (DAX Measures in Power BI)

| Measure Name | Description |
|---------------|-------------|
| **Avg Rating** | Average of `rating`. |
| **% Positive** | `COUNT(sentiment_label="Positive") / COUNT(review_id)`. |
| **Sentiment Index** | `(Positive – Negative)/Total Reviews`. |
| **UX Health Score** | Average of `ux_usability_sentiment`, `ux_navigation_sentiment`, `ux_performance_sentiment`. |
| **Complaints per 1k Reviews** | Theme-specific complaints × 1000 / total reviews. |
| **Review Volume MoM Growth %** | Month-over-month change in review count. |

---

## 6️⃣ Data Quality Assurance  

| Check | Threshold | Method |
|--------|------------|--------|
| Missing critical fields | < 5 % nulls | Pandas `isnull()` check |
| Duplicate reviews | 0 duplicates | SHA256 hash match on text+date |
| Sentiment validation | ≥ 85 % agreement vs AppFollow semantic score | Manual QA sample of 1 000 |
| UX tagging accuracy | 80 – 90 % precision via manual validation | Cross-checked taxonomy sample |

---

## 7️⃣ Usage Notes  

* For performance dashboards, join **FactReviews** to DimVersion and DimPlatform.  
* For UX dashboards, use pre-aggregated BigQuery views (e.g., `ux_metrics`).  
* Sensitive fields such as usernames are excluded to maintain GDPR compliance.  

---

## 8️⃣ References  

* [Product Requirement Document v1.4](../docs/Product_Requirement_Document-final.pdf)  
* [GDPR Compliance Statement](../docs/GDPR_Compliance.md)  

[//]: # (* [themes.yml – Feature Taxonomy]&#40;../config/themes.yml&#41;)

---

© 2025 James O. Adeshina · All data processed under legitimate interest for aggregate analytics only.