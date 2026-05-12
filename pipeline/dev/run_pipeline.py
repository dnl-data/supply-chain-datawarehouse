#!/usr/bin/env python3
"""
Supply Chain Data Warehouse - Main Pipeline
Executes the complete ELT pipeline from extraction to gold layer
"""

import subprocess
import sys
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def run_command(command, description):
    """Execute a shell command and handle errors"""
    print(f"\n{'='*60}")
    print(f"▶ {description}...")
    print(f"{'='*60}")
    
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    
    if result.returncode == 0:
        print(f"✅ {description} completed successfully")
        if result.stdout:
            print(result.stdout[-500:])  # Show last 500 chars of output
        return True
    else:
        print(f"❌ {description} failed with error code {result.returncode}")
        if result.stderr:
            print(f"Error details:\n{result.stderr[-1000:]}")
        return False

def main():
    """Main pipeline orchestration"""
    print("\n" + "="*60)
    print("🏭 SUPPLY CHAIN DATA WAREHOUSE - ELT PIPELINE")
    print("="*60)
    
    # Step 1: Extract data from Kaggle to S3
    if not run_command("python pipeline/dev/extraction.py", "EXTRACTION (Kaggle → S3 Bronze)"):
        print("\n❌ Pipeline stopped at EXTRACTION stage")
        sys.exit(1)
    
    # Step 2: Validate Bronze layer
    if not run_command("python pipeline/dev/validation.py", "VALIDATION (Bronze layer schema)"):
        print("\n❌ Pipeline stopped at VALIDATION stage")
        sys.exit(1)
    
    # Step 3: Transform Bronze → Silver
    if not run_command("python -c \"import duckdb; duckdb.execute(open('sql_transformation/dev/silver.sql').read()); print('Silver tables created successfully')\"", "TRANSFORMATION (Bronze → Silver with DuckDB)"):
        print("\n❌ Pipeline stopped at SILVER stage")
        sys.exit(1)
    
    # Step 4: Transform Silver → Gold
    if not run_command("python -c \"import duckdb; duckdb.execute(open('sql_transformation/dev/gold.sql').read()); print('Gold tables created successfully')\"", "TRANSFORMATION (Silver → Gold with DuckDB)"):
        print("\n❌ Pipeline stopped at GOLD stage")
        sys.exit(1)
    
    # Final success message
    print("\n" + "="*60)
    print("🎉 PIPELINE EXECUTED SUCCESSFULLY! 🎉")
    print("="*60)
    print("\n📊 Final data locations:")
    print("  📁 Local (GitHub preview): data/dev/bronze/, data/dev/silver/, data/dev/gold/")
    print("  ☁️  Cloud (S3): s3://supply-chain-dwh/test/bronze/, silver/, gold/")
    print("\n✅ All layers (Bronze, Silver, Gold) are ready for analysis!")
    sys.exit(0)

if __name__ == "__main__":
    main()