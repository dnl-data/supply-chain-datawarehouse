import kagglehub
import os
import shutil

def download_kaggle_files(kaggle_path, save_path):
    # Check if files already exist in destination
    if os.path.exists(save_path) and os.listdir(save_path):
        print(f"Files already exist in '{save_path}' folder. Skipping download.")
        return
    
    try:
        # Downloading the dataset
        downloaded_path = kagglehub.dataset_download(kaggle_path)
        # Creating destination folder if it doesn't exist
        os.makedirs(save_path, exist_ok=True)
        
    except Exception as e:
        print(f"An error occurred during download: {e}")
        return
        
    else:
        # Copying all files from downloaded path to save_path
        for filename in os.listdir(downloaded_path):
            source_file = os.path.join(downloaded_path, filename)
            destination_file = os.path.join(save_path, filename)
            shutil.copy2(source_file, destination_file)

        print(f"Files copied successfully to: '{save_path}'folder ")

# Call the function
download_kaggle_files(
    "rajhkumarr/e-commerce-and-retail-supply-chain",
    "data"
)