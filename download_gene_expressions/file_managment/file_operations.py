import os
import time
import gzip
import shutil
from file_managment.path_config import user_path

download_path = user_path('Downloads')

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

def extract_gz_file(file_name, from_dir, to_dir):
    gz_file_path = os.path.join(download_path, file_name)
    extracted_file_name = os.path.splitext(file_name)[0]
    extracted_file_path = os.path.join(to_dir, extracted_file_name)

    wait_until_file_is_available(gz_file_path)

    try:
        with gzip.open(gz_file_path, 'rb') as gz_file:
            with open(extracted_file_path, 'wb') as extracted_file:
                shutil.copyfileobj(gz_file, extracted_file)
        shutil.move(gz_file_path, os.path.join(from_dir, file_name))
    except Exception as e:
        raise Exception(f"Failed to extract {file_name}: {e}")

def process_gz_files(from_dir, to_dir):
    for file_name in os.listdir(download_path):
        if file_name.endswith('.gz'):
            extract_gz_file(file_name, from_dir, to_dir)

