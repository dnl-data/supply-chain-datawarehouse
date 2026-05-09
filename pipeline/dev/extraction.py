from dotenv import load_dotenv
load_dotenv()  
import kagglehub
import os
import shutil
import boto3
from config import KAGGLE_DATASET_PATH, S3_BUCKET_NAME, S3_FOLDER, EXPECTED_SCHEMA

def download_kaggle_files(kaggle_path, s3_bucket, s3_folder="test"):
    """
    Download dataset from Kaggle, save locally with 'bronze_' prefix, and upload files to AWS S3
    """
    s3_client = boto3.client('s3')
    
    try:
        # Download Kaggle dataset (goes to cache folder)
        print(f"Downloading dataset from Kaggle...")
        downloaded_path = kagglehub.dataset_download(kaggle_path)

        # Create local dev folder if it doesn't exist
        local_dev_folder = "data/dev/bronze"
        os.makedirs(local_dev_folder, exist_ok=True)

        # Get expected table names from EXPECTED_SCHEMA
        expected_tables = list(EXPECTED_SCHEMA.keys())

        # Process each file
        file_count = 0
        for filename in os.listdir(downloaded_path):
            source_file = os.path.join(downloaded_path, filename)
            
            # Determine the bronze filename based on expected schema
            base_name = os.path.splitext(filename)[0]
            bronze_filename = None
            
            # Try to match with expected tables
            for table in expected_tables:
                table_base = table.replace("bronze_", "").replace("bronze.", "")
                if table_base == base_name or table_base in base_name:
                    bronze_filename = f"{table}.csv"
                    break
            
            # If no match found, use generic naming
            if bronze_filename is None:
                bronze_filename = f"bronze_{filename}"
            
            # Local save
            local_dest = os.path.join(local_dev_folder, bronze_filename)
            shutil.copy2(source_file, local_dest)
            print(f"Saved locally: {local_dest}")

            # Upload to S3
            s3_key = f"{s3_folder}/bronze/bronze_{filename}"
            s3_client.upload_file(source_file, s3_bucket, s3_key)
            print(f"Uploaded to S3: {s3_key}")
            
            file_count += 1

        print(f"{file_count} files saved locally in '{local_dev_folder}'")
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
        print("Files saved locally and uploaded to S3 successfully!")
    else:
        print("Process failed")