import os
import time
import gzip
import shutil
import csv
from file_managment.path_config import user_path

download_path = user_path('Downloads')
GENES_OF_INTEREST = [
    "C6orf150", "CCL5", "CXCL10", "TMEM173",
    "CXCL9", "CXCL11", "NFKB1", "IKBKE",
    "IRF3", "TREX1", "ATM", "IL6", "IL8"
]

def check_active_downloads(download_path):
    return any([fname.endswith(".crdownload") for fname in os.listdir(download_path)])

def wait_for_all_downloads(timeout=500):
    start_time = time.time()
    while time.time() - start_time < timeout:
        if not check_active_downloads(download_path):
            return True
        time.sleep(1)
    return False

def wait_until_file_is_available(file_path, timeout=60):
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            with open(file_path, 'rb') as file:
                return True
        except IOError:
            time.sleep(1)
    raise Exception(f"Timeout waiting for file to become available: {file_path}")

def manipulate_files(file_name, zipped_folder, unzipped_folder, processed_folder):
    gz_file_path = os.path.join(download_path, file_name)
    extracted_file_name = os.path.splitext(file_name)[0]
    extracted_file_path = os.path.join(unzipped_folder, extracted_file_name)

    wait_until_file_is_available(gz_file_path)

    try:
        with gzip.open(gz_file_path, 'rb') as gz_file:
            with open(extracted_file_path, 'wb') as extracted_file:
                shutil.copyfileobj(gz_file, extracted_file)
        shutil.move(gz_file_path, os.path.join(zipped_folder, file_name))

        processed_file_name = f"processed_{extracted_file_name}"
        processed_file_path = os.path.join(processed_folder, processed_file_name)

        manipulate_and_save_tsv(extracted_file_path, processed_file_path)
    except Exception as e:
        raise Exception(f"Failed to extract {file_name}: {e}")

def manipulate_and_save_tsv(input_file_path, output_file_path):
    try:
        with open(input_file_path, 'r') as tsv_file:
            reader = csv.reader(tsv_file, delimiter='\t')
            header = next(reader)

            sample_ids = header[1:]  
            gene_data = {gene: [] for gene in GENES_OF_INTEREST}

            for row in reader:
                gene_name = row[0]
                if gene_name in GENES_OF_INTEREST:
                    gene_data[gene_name] = row[1:]  

        transposed_data = list(zip(*([["Gene"] + sample_ids] + [[gene] + gene_data[gene] for gene in GENES_OF_INTEREST])))

        with open(output_file_path, 'w', newline='') as tsv_output:
            writer = csv.writer(tsv_output, delimiter='\t')
            writer.writerows(transposed_data)

    except Exception as e:
        raise Exception(f"Failed to manipulate data in {input_file_path}: {e}")

def process_gz_files(gz_folder, unzipped_folder, processed_folder):
    for file_name in os.listdir(download_path):
        if file_name.endswith('.gz'):
            manipulate_files(file_name, gz_folder, unzipped_folder, processed_folder)