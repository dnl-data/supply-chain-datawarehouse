from dotenv import load_dotenv
load_dotenv()  
import kagglehub
import os
import boto3
from config import KAGGLE_DATASET_PATH, S3_BUCKET_NAME, S3_FOLDER

def download_kaggle_files(kaggle_path, s3_bucket, s3_folder="test"):
    """
    Download dataset from Kaggle and upload files directly to AWS S3
    No local storage - cloud only
    """
    s3_client = boto3.client('s3')
    
    try:
        # Download Kaggle dataset (goes to cache folder)
        print(f"Downloading dataset from Kaggle...")
        downloaded_path = kagglehub.dataset_download(kaggle_path)

        # Process each file
        file_count = 0
        for filename in os.listdir(downloaded_path):
            source_file = os.path.join(downloaded_path, filename)
            
            # Upload to S3
            s3_key = f"{s3_folder}/bronze/bronze_{filename}"
            s3_client.upload_file(source_file, s3_bucket, s3_key)
            print(f"Uploaded to S3: {s3_key}")
            file_count += 1

        print(f"{file_count} files uploaded to s3://{s3_bucket}/{s3_folder}/bronze/")
        return "uploaded"
        
    except Exception as e:
        print(f"Error: {e}")
        return "failed"

if __name__ == "__main__":
    result = download_kaggle_files(
        KAGGLE_DATASET_PATH,
        S3_BUCKET_NAME,
        S3_FOLDER
    )
    
    if result == "uploaded":
        print("Files uploaded to S3 successfully!")
    else:
        print("Process failed")