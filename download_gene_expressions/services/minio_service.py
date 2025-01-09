from minio import Minio
from minio.error import S3Error
import os

MINIO_BASE_URL = "regoch.net:9000"
ACCESS_KEY = "minioAdmin"
SECRET_KEY = "supersecretpassword"
BUCKET_NAME = "antonela-aabicic-p2"

minio_client = Minio(MINIO_BASE_URL, access_key=ACCESS_KEY, secret_key=SECRET_KEY, secure=False)

def ensure_bucket_exists(bucket_name):
    if not minio_client.bucket_exists(bucket_name):
        minio_client.make_bucket(bucket_name)

def upload_to_minio(local_file_path, object_name):
    try:
        if not os.path.exists(local_file_path):
            print(f"File does not exist: {local_file_path}")
            return

        ensure_bucket_exists(BUCKET_NAME)
        minio_client.fput_object(bucket_name=BUCKET_NAME, object_name=object_name, file_path=local_file_path)
    except S3Error as err:
        print(f"Error uploading to MinIO: {err}")

def list_files_in_bucket(bucket_name):
    objects = list(minio_client.list_objects(bucket_name))
    return [obj.object_name for obj in objects]
