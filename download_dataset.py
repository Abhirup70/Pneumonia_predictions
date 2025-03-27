import os
import kaggle
from kaggle.api.kaggle_api_extended import KaggleApi
import zipfile
import sys
import time

def download_dataset():
    # Initialize the Kaggle API
    api = KaggleApi()
    
    try:
        # Check if kaggle.json exists
        kaggle_dir = os.path.expanduser('~/.kaggle')
        kaggle_json = os.path.join(kaggle_dir, 'kaggle.json')
        
        if not os.path.exists(kaggle_json):
            print(f"Error: kaggle.json not found at {kaggle_json}")
            print("Please download kaggle.json from your Kaggle account settings")
            return
            
        # Authenticate using your kaggle.json credentials
        print("Attempting to authenticate with Kaggle...")
        api.authenticate()
        print("Successfully authenticated with Kaggle")
        
        # Create a data directory if it doesn't exist
        data_dir = os.path.join(os.getcwd(), 'data')
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)
            print(f"Created data directory at: {data_dir}")
        
        # Download the dataset
        print("Starting dataset download...")
        print(f"Downloading to: {data_dir}")
        
        # Get dataset information first
        print("Fetching dataset information...")
        dataset = api.dataset_get('paultimothymooney/chest-xray-pneumonia')
        print(f"Dataset size: {dataset.size} bytes")
        
        # Download with progress updates
        print("\nInitiating download (this may take several minutes)...")
        print("Download progress will be shown below:")
        
        # Download the dataset
        api.dataset_download_files(
            'paultimothymooney/chest-xray-pneumonia',
            path=data_dir,
            unzip=False
        )
        
        print("\nDownload completed!")
        
        # Find the downloaded zip file
        zip_files = [f for f in os.listdir(data_dir) if f.endswith('.zip')]
        if not zip_files:
            print("Error: No zip file was downloaded")
            return
            
        zip_file = os.path.join(data_dir, zip_files[0])
        print(f"\nFound downloaded zip file: {zip_file}")
        
        # Extract the zip file
        print("\nExtracting zip file (this may take a few minutes)...")
        with zipfile.ZipFile(zip_file, 'r') as zip_ref:
            total_files = len(zip_ref.namelist())
            for idx, file in enumerate(zip_ref.namelist(), 1):
                zip_ref.extract(file, data_dir)
                if idx % 100 == 0:  # Show progress every 100 files
                    print(f"Extracted {idx}/{total_files} files...")
            
        # Remove the zip file after extraction
        os.remove(zip_file)
        print("\nRemoved zip file after extraction")
        
        # Verify the extraction
        extracted_dirs = os.listdir(data_dir)
        print("\nExtracted directories:")
        for dir_name in extracted_dirs:
            print(f"- {dir_name}")
        
        print("\nDataset downloaded and extracted successfully!")
        print(f"The dataset is now available in: {data_dir}")
        
    except Exception as e:
        print(f"\nAn error occurred: {str(e)}")
        print("\nPlease make sure you have:")
        print("1. A Kaggle account")
        print("2. Downloaded kaggle.json from your Kaggle account settings")
        print("3. Placed kaggle.json in ~/.kaggle/ directory")
        print("4. Set appropriate permissions for kaggle.json (chmod 600)")
        print("\nFor Windows users:")
        print("The kaggle.json should be in: C:\\Users\\<YourUsername>\\.kaggle\\kaggle.json")
        
        # Additional debugging information
        print("\nDebugging information:")
        print(f"Current working directory: {os.getcwd()}")
        print(f"Data directory exists: {os.path.exists(data_dir)}")
        if os.path.exists(data_dir):
            print("Contents of data directory:")
            print(os.listdir(data_dir))

if __name__ == "__main__":
    download_dataset() 