# Root Dockerfile for default container build (delegates to backend)
# ==============================================================================
# Ritucast Backend Production Dockerfile (Multi-Stage Build)
# ==============================================================================

FROM python:3.10-slim-bookworm AS builder

WORKDIR /build

RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc g++ libffi-dev && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir --prefix=/install -r requirements.txt

FROM python:3.10-slim-bookworm AS runtime

LABEL maintainer="Ritucast Platform Engineering Team <engineering@ritucast.app>"
LABEL description="Ritucast Agricultural Intelligence Backend API"

WORKDIR /app

RUN groupadd -g 10001 ritucast && \
    useradd -u 10001 -g ritucast -s /bin/bash -m ritucast

COPY --from=builder /install /usr/local

COPY --chown=ritucast:ritucast api/ /app/api/
COPY --chown=ritucast:ritucast analytics/ /app/analytics/
COPY --chown=ritucast:ritucast pipelines/ /app/pipelines/
COPY --chown=ritucast:ritucast data/processed/ /app/data/processed/
COPY --chown=ritucast:ritucast data/sample/ /app/data/sample/

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app \
    PORT=8000 \
    ENVIRONMENT=production

USER ritucast

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD python3 -c "import urllib.request, os; port = os.environ.get('PORT', '8000'); urllib.request.urlopen(f'http://127.0.0.1:{port}/health')" || exit 1

CMD ["sh", "-c", "exec uvicorn api.main:app --host 0.0.0.0 --port ${PORT:-8000} --workers 2 --access-log"]
