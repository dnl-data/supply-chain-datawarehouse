"""
Unit test for S3 connection and read access
Does NOT write anything to S3 - safe to run anytime
"""

import os
import boto3
from dotenv import load_dotenv

# Load credentials from .env file
load_dotenv()

def test_s3_credentials():
    """Test if AWS credentials are properly configured"""
    print("\n--- Test: AWS Credentials ---")
    
    try:
        session = boto3.Session()
        credentials = session.get_credentials()
        
        if credentials:
            print(f"✅ AWS credentials found (access key: {credentials.access_key[:6]}...)")
            print(f"   Region: {session.region_name or 'default'}")
            return True
        else:
            print("❌ No AWS credentials found")
            return False
            
    except Exception as e:
        print(f"❌ Error checking credentials: {e}")
        return False

def test_s3_bucket_access():
    """Test if bucket exists and is accessible"""
    print("\n--- Test: S3 Bucket Access ---")
    
    try:
        s3_client = boto3.client('s3')
        bucket_name = os.getenv('S3_BUCKET_NAME', 'supply-chain-dwh')
        
        # Try to list bucket contents (max 1 object)
        response = s3_client.list_objects_v2(Bucket=bucket_name, MaxKeys=1)
        
        print(f"✅ Bucket '{bucket_name}' is accessible")
        return True
        
    except Exception as e:
        print(f"❌ Cannot access bucket: {e}")
        return False

def test_s3_list_files():
    """Test listing files in the bronze folder"""
    print("\n--- Test: S3 List Files ---")
    
    try:
        s3_client = boto3.client('s3')
        bucket_name = os.getenv('S3_BUCKET_NAME', 'supply-chain-dwh')
        s3_folder = os.getenv('S3_FOLDER', 'test')
        
        prefix = f"{s3_folder}/bronze/"
        response = s3_client.list_objects_v2(Bucket=bucket_name, Prefix=prefix)
        
        if 'Contents' in response:
            file_count = len(response['Contents'])
            print(f"✅ Found {file_count} files in s3://{bucket_name}/{prefix}")
            for obj in response['Contents'][:5]:  # Show first 5
                print(f"   - {obj['Key']}")
            return True
        else:
            print(f"⚠️ No files found in s3://{bucket_name}/{prefix}")
            return False
            
    except Exception as e:
        print(f"❌ Cannot list files: {e}")
        return False

def test_s3_read_file():
    """Test reading a single small file from S3"""
    print("\n--- Test: S3 Read File ---")
    
    try:
        s3_client = boto3.client('s3')
        bucket_name = os.getenv('S3_BUCKET_NAME', 'supply-chain-dwh')
        s3_folder = os.getenv('S3_FOLDER', 'test')
        
        # Try to read one existing file (suppliers is small)
        test_key = f"{s3_folder}/bronze/bronze_suppliers.csv"
        
        response = s3_client.get_object(Bucket=bucket_name, Key=test_key)
        content = response['Body'].read()
        
        print(f"✅ Successfully read s3://{bucket_name}/{test_key}")
        print(f"   File size: {len(content)} bytes")
        return True
        
    except Exception as e:
        print(f"❌ Cannot read file: {e}")
        print(f"   Make sure the bucket contains {test_key}")
        return False

if __name__ == "__main__":
    print("\n" + "="*50)
    print("S3 CONNECTION UNIT TESTS")
    print("="*50)
    
    results = []
    
    results.append(("Credentials", test_s3_credentials()))
    results.append(("Bucket Access", test_s3_bucket_access()))
    results.append(("List Files", test_s3_list_files()))
    results.append(("Read File", test_s3_read_file()))
    
    print("\n" + "="*50)
    print("TEST RESULTS SUMMARY")
    print("="*50)
    
    all_passed = True
    for name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status} - {name}")
        if not passed:
            all_passed = False
    
    print("="*50)
    
    if all_passed:
        print("\n All S3 connection tests passed!")
        exit(0)
    else:
        print("\n Some tests failed. Check your AWS configuration.")
        exit(1)