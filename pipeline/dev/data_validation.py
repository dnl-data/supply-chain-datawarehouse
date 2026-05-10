from dotenv import load_dotenv
load_dotenv()

import pandas as pd
import boto3
from config import EXPECTED_SCHEMA, S3_BUCKET_NAME, S3_FOLDER

def read_csv_from_s3(bucket, key):
    """
    Read a CSV file directly from S3 and return a DataFrame
    """
    try:
        s3_client = boto3.client('s3')
        obj = s3_client.get_object(Bucket=bucket, Key=key)
        return pd.read_csv(obj['Body'])
    except Exception as e:
        print(f"Error reading s3://{bucket}/{key}: {e}")
        return None

def validate_schema():
    """
    Validate CSV files directly from S3 against expected schema from config.py
    """
    expected_tables = EXPECTED_SCHEMA.keys()
    all_valid = True
    
    print("\n=== SCHEMA VALIDATION STARTED (S3) ===\n")
    print(f"Reading from: s3://{S3_BUCKET_NAME}/{S3_FOLDER}/bronze/\n")
    
    for table_name in expected_tables:
        # Build S3 key (path to bronze CSV)
        s3_key = f"{S3_FOLDER}/bronze/{table_name}.csv"
        
        # Read CSV from S3
        df = read_csv_from_s3(S3_BUCKET_NAME, s3_key)
        
        if df is None:
            print(f"MISSING: {table_name}.csv not found in S3")
            all_valid = False
            continue
        
        expected_columns = EXPECTED_SCHEMA[table_name]
        
        # Check columns
        missing_cols = set(expected_columns.keys()) - set(df.columns)
        extra_cols = set(df.columns) - set(expected_columns.keys())
        
        if missing_cols:
            print(f"{table_name}: Missing columns: {missing_cols}")
            all_valid = False
        if extra_cols:
            print(f"{table_name}: Extra columns found: {extra_cols}")
        
        # Quick type validation (basic)
        type_errors = []
        for col, dtype in expected_columns.items():
            if col in df.columns:
                try:
                    if dtype == "DATE":
                        pd.to_datetime(df[col])
                    elif dtype in ["INTEGER", "BIGINT"]:
                        pd.to_numeric(df[col], errors='coerce')
                    elif dtype == "DOUBLE":
                        pd.to_numeric(df[col], errors='coerce')
                except Exception as e:
                    type_errors.append(f"{col}: {e}")
        
        if type_errors:
            print(f"{table_name}: Type conversion errors: {type_errors}")
            all_valid = False
        else:
            print(f"{table_name}: Validated ({len(df)} rows, {len(expected_columns)} columns)")
    
    print("\n=== VALIDATION COMPLETED ===")
    
    if all_valid:
        print("All tables passed validation!")
    else:
        print("Validation failed. Check errors above.")
    
    return all_valid

if __name__ == "__main__":
    print("Validating bronze layer data from S3...")
    success = validate_schema()
    
    if success:
        print("\n Data is ready for silver transformation!")
    else:
        print("\n Fix the issues above before proceeding to silver.")