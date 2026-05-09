import kagglehub
import os
import boto3
from config import KAGGLE_DATASET_PATH,S3_BUCKET_NAME,S3_FOLDER

def download_kaggle_files_to_s3(kaggle_path, s3_bucket, s3_folder="data/test"):
    """
    Download dataset from Kaggle and upload files to AWS S3
    """
    s3_client = boto3.client('s3')
    
    try:
        # Download Kaggle dataset (goes to cache folder)
        print(f"Downloading dataset from Kaggle...")
        downloaded_path = kagglehub.dataset_download(kaggle_path)
        
        # Upload each file to S3
        file_count = 0
        for filename in os.listdir(downloaded_path):
            source_file = os.path.join(downloaded_path, filename)
            s3_key = f"{s3_folder}/{filename}"
            
            s3_client.upload_file(source_file, s3_bucket, s3_key)  # ← FIXED: s3_bucket not s3_folder
            print(f"Uploaded: {filename}")
            file_count += 1

        print(f"{file_count} files uploaded to s3://{s3_bucket}/{s3_folder}")
        return "uploaded"
        
    except Exception as e:
        print(f"Error: {e}")
        return "failed"

if __name__ == "__main__":
    result = download_kaggle_files_to_s3(
        KAGGLE_DATASET_PATH,
        S3_BUCKET_NAME,  # See config.py
        S3_FOLDER
    )
    
    if result == "uploaded":
        print("Files uploaded to S3 successfully!")
    else:
        print("Upload failed")