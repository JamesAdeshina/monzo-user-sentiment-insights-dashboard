#%%
# ------------------------------------------------------------
# 04_bigquery_upload.ipynb — Authentication & Setup
# ------------------------------------------------------------

from google.cloud import bigquery
from google.oauth2 import service_account
import pandas as pd
import os

# Path to your service account key
key_path = "../credentials/monzo-data-uploader-d16b82e5caaf.json"

# Verify the file exists
assert os.path.exists(key_path), "❌ Key file not found. Please check the path."
#%%
# Authenticate using the service account
credentials = service_account.Credentials.from_service_account_file(key_path)
project_id = "monzo-data-uploader"  # Your GCP project ID

# Initialize the BigQuery client
client = bigquery.Client(credentials=credentials, project=project_id)

print(f"✅ Successfully connected to BigQuery project: {project_id}")

#%%
# ------------------------------------------------------------
# Upload warehouse tables to BigQuery
# ------------------------------------------------------------
from google.cloud import bigquery

DATA_DIR = "../data/warehouse/parquet"
DATASETS = {
    "FactReviews": f"{DATA_DIR}/FactReviews.csv",
    "DimPlatform": f"{DATA_DIR}/DimPlatform.csv",
    "DimVersion": f"{DATA_DIR}/DimVersion.csv",
    "DimDate": f"{DATA_DIR}/DimDate.csv",
    "DimSentiment": f"{DATA_DIR}/DimSentiment.csv"
}

# Create (or use existing) dataset
dataset_id = f"{project_id}.monzo_reviews"
dataset = bigquery.Dataset(dataset_id)
dataset.location = "europe-west2"  # or 'US' depending on your region
#%%
try:
    client.create_dataset(dataset)
    print(f"✅ Created dataset: {dataset_id}")
except Exception as e:
    print(f"⚠️ Dataset may already exist: {e}")

# Upload each table
for table_name, csv_path in DATASETS.items():
    table_id = f"{dataset_id}.{table_name}"
    df = pd.read_csv(csv_path)

    job_config = bigquery.LoadJobConfig(
        autodetect=True,
        source_format=bigquery.SourceFormat.CSV,
        write_disposition="WRITE_TRUNCATE",
        skip_leading_rows=1,
        field_delimiter=",",
        quote_character=None,        # 🚨 disables quote enforcement
        encoding="UTF-8",
        allow_quoted_newlines=True,  # ✅ allows line breaks inside reviews
        ignore_unknown_values=True   # ✅ ignores extra commas or misquotes
    )

    with open(csv_path, "rb") as source_file:
        job = client.load_table_from_file(source_file, table_id, job_config=job_config)

    job.result()
    print(f"✅ Uploaded {table_name} → {table_id} ({len(df)} rows)")

#%%
for table in client.list_tables(dataset_id):
    print(f"📊 {table.table_id}")

#%%
