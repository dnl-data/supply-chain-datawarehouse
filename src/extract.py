import kagglehub
import os
import shutil

def download_kaggle_files(kaggle_path, save_path):
    """
    Download dataset from Kaggle and copy files to specified folder
    
    Args:
        kaggle_path (str): Kaggle dataset identifier (username/dataset-name)
        save_path (str): Local folder path where files will be copied
    
    Returns:
        str: "skipped", "downloaded", or "failed"
    """
    # Check if files already exist in destination
    if os.path.exists(save_path) and os.listdir(save_path):
        print(f"Files already exist in '{save_path}' folder. Skipping download.")
        return "skipped"
    
    try:
        # Downloading the dataset to cache
        print(f"Downloading dataset from Kaggle...")
        downloaded_path = kagglehub.dataset_download(kaggle_path)
        
        # Creating destination folder if it doesn't exist
        os.makedirs(save_path, exist_ok=True)
        
        # Copying all files from downloaded path to save_path
        file_count = 0
        for filename in os.listdir(downloaded_path):
            source_file = os.path.join(downloaded_path, filename)
            destination_file = os.path.join(save_path, filename)
            shutil.copy2(source_file, destination_file)
            file_count += 1

        print(f"{file_count} files copied successfully to: '{save_path}' folder")
        return "downloaded"
        
    except Exception as e:
        print(f"An error occurred during download: {e}")
        return "failed"

if __name__ == "__main__":
    extraction = download_kaggle_files(
        "rajhkumarr/e-commerce-and-retail-supply-chain",
        "data"
    )
    
    if extraction == "skipped":
        print("No action needed.")
    elif extraction == "downloaded":
        print("New files downloaded successfully.")
    else:
        print("Extraction failed - check the error message above")