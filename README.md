# Monzo User Sentiment & Feature Insights Dashboard

**Author:** James Adeshina  
**Date:** November 2025  
**Version:** 1.4  


Quick Info & Badges
<p align="left"> <!-- Core Stack --> <img src="https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&logoColor=white" alt="Python Badge"/> <img src="https://img.shields.io/badge/Power%20BI-Dashboard-F2C811?logo=power-bi&logoColor=black" alt="Power BI Badge"/> <img src="https://img.shields.io/badge/Google%20BigQuery-Data%20Warehouse-669DF6?logo=google-cloud&logoColor=white" alt="BigQuery Badge"/> <img src="https://img.shields.io/badge/NLP-Sentiment%20Analysis-ff69b4?logo=ai&logoColor=white" alt="NLP Badge"/> <!-- Tools --> <img src="https://img.shields.io/badge/Pandas-Data%20Processing-150458?logo=pandas&logoColor=white" alt="Pandas Badge"/> <img src="https://img.shields.io/badge/VADER-Lexicon%20Sentiment-orange" alt="VADER Badge"/> <img src="https://img.shields.io/badge/YAKE-Keyphrase%20Extraction-ffcc00" alt="YAKE Badge"/> <img src="https://img.shields.io/badge/KeyBERT-Topic%20Modeling-8A2BE2" alt="KeyBERT Badge"/> <!-- Compliance & Documentation --> <img src="https://img.shields.io/badge/GDPR-Compliant-brightgreen?logo=security&logoColor=white" alt="GDPR Badge"/> <img src="https://img.shields.io/badge/License-MIT-lightgrey" alt="License Badge"/> <img src="https://img.shields.io/badge/Status-Portfolio%20Project-success" alt="Status Badge"/> </p>


## Summary
Transforming 33,500+ Monzo app store reviews (2015–2025) into actionable insights through NLP, Power BI, and BigQuery, empowering Product, UX, and HR teams with real-time customer sentiment and usability intelligence.

## Overview

This project transforms over **33,500 Monzo app store reviews (2015–2025)** from the Apple App Store and Google Play Store into a unified **Power BI Insights Dashboard**.  

By combining **Natural Language Processing (NLP)**, **Google BigQuery**, and **Power BI**, the project converts unstructured customer feedback into actionable intelligence that informs **Product**, **UX Research**, and **HR** teams.  

It demonstrates end-to-end data capability — from **ETL & NLP** to **data warehousing** and **BI visualization**, while maintaining **GDPR-compliant data practices**.


## Project Objectives

- **Unify Review Data**: Integrate ~33.5k app store reviews across iOS and Android into a single clean dataset.  
- **Analyse Customer Sentiment**: Apply NLP (VADER, YAKE) to classify sentiment and extract Monzo-specific themes (e.g., *Flex, Pots, Onboarding, Support*).  
- **Enrich UX Insights**: Tag reviews with UX dimensions (Usability, Navigation, Performance, Accessibility, Emotional Response).  
- **Visualize in Power BI**: Build an interactive dashboard to explore sentiment trends, feature feedback, and UX patterns.  
- **Ensure Data Ethics**: Comply fully with GDPR principles via anonymization and secure storage.


## Tech Stack

| Layer | Tools & Technologies |
|-------|----------------------|
| **Data Source** | AppFollow Exports (Apple App Store, Google Play Store) |
| **Processing** | Python, Pandas, NLTK, VADER, YAKE, KeyBERT |
| **Storage & Querying** | Google BigQuery (GDPR-compliant cloud warehouse) |
| **Visualization** | Power BI Desktop (DAX, Import Mode) |
| **Version Control** | GitHub |
| **File Formats** | CSV, Parquet |


## Project Structure

```
Monzo-Reviews-Dashboard/
│
├── data/
│ ├── raw/
│ │ ├── appstore/monzo_appstore_2015_2025.csv
│ │ └── googleplay/monzo_googleplay_2015_2019.csv ...
│ ├── interim/merged_appstore.csv
│ ├── processed/Monzo_Reviews_Master.parquet
│ └── sample/sample_appstore.csv
│
├── notebooks/
│ ├── 01_data_exploration.ipynb
│ ├── 02_data_cleaning.ipynb
│ ├── 03_sentiment_analysis.ipynb
│ ├── 04_theme_tagging.ipynb
│ └── 05_powerbi_prep.ipynb
│
├── scripts/
│ ├── merge_reviews.py
│ ├── clean_reviews.py
│ ├── sentiment_scoring.py
│ ├── theme_tagging.py
│ └── export_bigquery.py
│
├── config/
│ ├── themes.yml
│ └── settings.yaml
│
├── bi/
│ ├── Monzo_Insights_Dashboard.pbix
│ └── visuals/
│
├── docs/
│ ├── Product_Requirement_Document.pdf
│ ├── Executive_Summary.pdf
│ ├── Data_Dictionary.md
│ └── GDPR_Compliance.md
│
├── requirements.txt
├── README.md
└── .gitignore
```


## Key Insights Delivered

- **Cross-Platform Trends:** Sentiment comparison between iOS and Android users.  
- **Feature Themes:** Top praise (e.g., *Flex*, *Budgeting*) vs. common pain points (e.g., *Card Declines*, *Onboarding Friction*).  
- **UX Health Metrics:** Sentiment tracking across usability, performance, and accessibility categories.  
- **Empathy Insights:** Service-related themes informing HR training and customer experience improvement.


## Dashboard Overview (Power BI)

### Dashboard Pages
1. **Executive Overview** — Sentiment trends, KPIs, and UX Health Score.  
2. **Platform & Version Analysis** — Compare iOS vs Android performance and release stability.  
3. **Thematic Deep Dive** — Feature-level feedback visualization with sentiment breakdowns.  
4. **HR & CX Lens** — Support and empathy themes tied to customer experience.  
5. **UX Research Dashboard** — Detailed analysis of usability, navigation, and accessibility metrics.


## Sample Workflow

```python
# Load and clean review data
import pandas as pd

appstore = pd.read_csv('data/raw/appstore/monzo_appstore_2015_2025.csv')
googleplay = pd.read_csv('data/raw/googleplay/monzo_googleplay_2022_2025.csv')

appstore['platform'] = 'iOS'
googleplay['platform'] = 'Android'

merged = pd.concat([appstore, googleplay], ignore_index=True)
merged.to_csv('data/interim/merged_reviews.csv', index=False)

```

## GDPR & Ethics

- Reviews sourced via AppFollow, which operates under GDPR-compliant DPAs.
- Anonymization: Usernames, emails, or personal references are removed/pseudonymized.
- Lawful Basis: Legitimate interest for product and UX improvement (Article 6(1)(f)).
- No Profiling: Data used only for aggregated insights, not individual targeting.


## Project Timeline (2–4 Weeks)

| Week    | Milestone                                              |
|---------|--------------------------------------------------------|
| Week 1  | Data acquisition, unification, and BigQuery upload     |
| Week 2  | NLP sentiment analysis + UX tagging, schema validation |
| Week 3  | Power BI dashboard development                         |
| Week 4  | Documentation, executive summary, GitHub polish        |



## Repository Contents

| File / Folder                     | Description                                      |
|----------------------------------|--------------------------------------------------|
| `Product_Requirement_Document.pdf` | Full PRD (Version 1.4)                         |
| `Monzo_Insights_Dashboard.pbix`  | Interactive Power BI dashboard                   |
| `Monzo_Reviews_Master.parquet`   | Final processed dataset                          |
| `scripts/`                        | Python ETL, NLP, and export scripts              |
| `config/themes.yml`              | Monzo-specific taxonomy                          |
| `docs/GDPR_Compliance.md`        | Data ethics and compliance documentation         |


## Contact

James O. Adeshina
| United Kingdom
| LinkedIn
| Portfolio Website
| GitHub
