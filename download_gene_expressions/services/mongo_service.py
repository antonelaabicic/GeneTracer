from pymongo import MongoClient
import pandas as pd
from io import BytesIO
from services.minio_service import minio_client

MONGO_URI = "mongodb+srv://mongodb:mongodb@cluster0.cx9ea.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
DATABASE_NAME = "gene_data"
COLLECTION_NAME = "patients"

def ensure_mongo_connection():
    client = MongoClient(MONGO_URI)
    db = client[DATABASE_NAME]
    collection = db[COLLECTION_NAME]
    return collection

def check_data_exists():
    collection = ensure_mongo_connection()
    return collection.estimated_document_count() > 0

def insert_data_to_mongo(bucket_name, combined_file_name):
    try:
        response = minio_client.get_object(bucket_name, combined_file_name)
        combined_data = pd.read_csv(BytesIO(response.read()), sep="\t")
        response.close()
        response.release_conn()

        records = []
        for _, row in combined_data.iterrows():
            record = {
                "patient_id": row["patient_id"],
                "bcr_patient_barcode": row["bcr_patient_barcode"],
                "cancer_cohort": row["cancer_cohort"],
                "gene_expressions": {
                    "C6orf150": row["C6orf150"],
                    "CCL5": row["CCL5"],
                    "CXCL10": row["CXCL10"],
                    "TMEM173": row["TMEM173"],
                    "CXCL9": row["CXCL9"],
                    "CXCL11": row["CXCL11"],
                    "NFKB1": row["NFKB1"],
                    "IKBKE": row["IKBKE"],
                    "IRF3": row["IRF3"],
                    "TREX1": row["TREX1"],
                    "ATM": row["ATM"],
                    "IL6": row["IL6"],
                    "IL8": row["IL8"]
                },
                "DSS": "Alive" if row["DSS"] == 1 else "Dead",
                "OS": "Alive" if row["OS"] == 1 else "Dead",
                "clinical_stage": row["clinical_stage"]
            }
            records.append(record)

        collection = ensure_mongo_connection()
        collection.insert_many(records)
        print(f"Inserted {len(records)} records into MongoDB.")

    except Exception as e:
        print(f"Error inserting data to MongoDB: {e}")

def fetch_data_from_mongo():
    collection = ensure_mongo_connection()
    return list(collection.find({}, {"_id": 0}))  
