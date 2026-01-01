FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Create storage directory structure
RUN mkdir -p /app/storage/uploads /app/storage/processed

CMD ["python", "worker.py"]
