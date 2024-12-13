FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "from pymilvus import connections; connections.connect(host='milvus-standalone', port=19530)" || exit 1

CMD ["python", "main.py"]