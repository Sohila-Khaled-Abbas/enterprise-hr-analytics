# =============================================================================
# Enterprise Human Capital & Operational Efficiency Diagnostics
# Production Multi-Stage Dockerfile
# =============================================================================

FROM python:3.12-slim-bookworm AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app/src \
    ACCEPT_EULA=Y

WORKDIR /app

# Install system dependencies and Microsoft ODBC Driver 18 for SQL Server
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    gnupg2 \
    apt-transport-https \
    ca-certificates \
    unixodbc \
    unixodbc-dev \
    build-essential \
    && curl -fsSL https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor -o /usr/share/keyrings/microsoft-prod.gpg \
    && curl -fsSL https://packages.microsoft.com/config/debian/12/prod.list > /etc/apt/sources.list.d/mssql-release.list \
    && apt-get update \
    && ACCEPT_EULA=Y apt-get install -y --no-install-recommends msodbcsql18 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Python requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Security: non-root execution
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# Copy application assets
COPY --chown=appuser:appuser src/ ./src/
COPY --chown=appuser:appuser scripts/ ./scripts/
COPY --chown=appuser:appuser sql/ ./sql/
COPY --chown=appuser:appuser data/ ./data/

# Default entrypoint
ENTRYPOINT ["python", "-m", "enterprise_hr.cli"]
CMD ["healthcheck"]
