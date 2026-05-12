# Dockerfile.simple
FROM python:3.11-slim

WORKDIR /app

# Copy everything
COPY . .

# Install dependencies
RUN pip install kagglehub boto3 duckdb pandas python-dotenv

# Run pipeline
CMD ["python", "pipeline/run_pipeline.py"]