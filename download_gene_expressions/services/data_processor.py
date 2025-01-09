import pandas as pd
from io import BytesIO
from services.minio_service import minio_client, upload_to_minio, list_files_in_bucket

def check_files_in_bucket(bucket_name, required_file_count):
    files = list_files_in_bucket(bucket_name)
    if len(files) != required_file_count:
        print(f"Expected {required_file_count} files in bucket '{bucket_name}', but found {len(files)}.")
        return False
    return files

def extract_cancer_cohort(file_name):
    parts = file_name.split(".")
    return parts[1] if len(parts) > 1 else "Unknown"

def merge_gene_and_clinical_data(clinical_file_name, bucket_name):
    try:
        clinical_response = minio_client.get_object(bucket_name, clinical_file_name)
        clinical_data = pd.read_csv(BytesIO(clinical_response.read()), sep="\t")
        clinical_response.close()
        clinical_response.release_conn()

        clinical_data = clinical_data[["bcr_patient_barcode", "DSS", "OS", "clinical_stage"]]

        files = check_files_in_bucket(bucket_name, 37)
        if not files:
            return

        merged_data = []
        for file_name in files:
            if file_name == clinical_file_name:
                continue  

            try:
                response = minio_client.get_object(bucket_name, file_name)
                gene_data = pd.read_csv(BytesIO(response.read()), sep="\t")
                response.close()
                response.release_conn()

                if 'Gene' in gene_data.columns:
                    gene_data.rename(columns={'Gene': 'bcr_patient_barcode'}, inplace=True)

                cancer_cohort = extract_cancer_cohort(file_name)
                gene_data["cancer_cohort"] = cancer_cohort

                merged = gene_data.merge(clinical_data, on="bcr_patient_barcode", how="inner")
                merged["patient_id"] = range(1, len(merged) + 1)

                cols = ["patient_id", "bcr_patient_barcode", "cancer_cohort"] + \
                       [col for col in merged.columns if col not in ["patient_id", "bcr_patient_barcode", "cancer_cohort"]]
                merged = merged[cols]
                merged_data.append(merged)

            except Exception as e:
                print(f"Error reading or processing file {file_name}: {e}")
                continue

        combined_data = pd.concat(merged_data)

        combined_file = "combined_gene_clinical_data.tsv"
        combined_data.to_csv(combined_file, sep="\t", index=False)

        upload_to_minio(combined_file, combined_file)
        print(f"Combined data uploaded to MinIO as '{combined_file}'.")

    except Exception as e:
        print(f"Error during merge: {e}")
