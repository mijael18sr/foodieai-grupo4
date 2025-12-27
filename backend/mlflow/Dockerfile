# =============================================================================
# MLflow Server Dockerfile
# Backend: PostgreSQL | Artifacts: S3
# =============================================================================

FROM python:3.11-slim

WORKDIR /mlflow

# Install MLflow with PostgreSQL and S3 support
RUN pip install --no-cache-dir \
    mlflow==2.17.0 \
    psycopg2-binary \
    boto3

# Create mlflow user
RUN useradd -m -u 1000 mlflow && \
    chown -R mlflow:mlflow /mlflow

USER mlflow

# Expose MLflow UI port
EXPOSE 5000

# Default command (will be overridden by docker-compose)
CMD ["mlflow", "server", "--host", "0.0.0.0", "--port", "5000"]
