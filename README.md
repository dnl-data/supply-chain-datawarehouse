# Supply Chain Data Warehouse

## Project Overview

An end-to-end ELT pipeline that extracts e-commerce and retail supply chain data from Kaggle, stores it in AWS S3 (Bronze layer), cleans and transforms it (Silver layer), and models it into analytical data marts (Gold layer). The entire pipeline is containerized with Docker and automated with a single command.

## Architecture


## Data Marts

| Data Mart | Description | Key Tables |
|-----------|-------------|------------|
| **Stock & Inventory** | Stock levels, reorder alerts, coverage days | `fact_inventory`, `dim_product`, `dim_date` |
| **Sales Performance** | Revenue by channel, promo impact, customer segments | `fact_sales`, `dim_channel`, `dim_promo` |
| **Procurement** | Supplier performance, lead times, landed costs | `fact_purchase`, `dim_supplier` |

## Tech Stack

| Layer | Tools |
|-------|-------|
| Orchestration | Python |
| Extraction | KaggleHub |
| Storage | AWS S3 |
| Transformation | DuckDB (SQL) |
| Containerization | Docker |
| Version Control | Git + GitHub |

## Quick Start

### Prerequisites

- Python 3.11+
- Docker (optional)
- AWS account with S3 bucket
- Kaggle account (API credentials)

### Environment Setup

```bash
# Clone repository
git clone https://github.com/dnl-data/supply-chain-datawarehouse.git
cd supply-chain-datawarehouse

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure AWS credentials
cp .env.example .env
# Edit .env with your AWS and Kaggle credentials
