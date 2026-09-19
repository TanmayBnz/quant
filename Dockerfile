FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    APP_PATH=apps/backtester/app.py

WORKDIR /app

COPY pyproject.toml README.md ./
COPY src ./src
RUN pip install --no-cache-dir .

COPY apps ./apps
COPY docs ./docs
COPY strategies ./strategies

EXPOSE 8501

CMD streamlit run "$APP_PATH" --server.address=0.0.0.0 --server.port=8501
