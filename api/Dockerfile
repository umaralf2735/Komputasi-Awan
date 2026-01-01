FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Create storage directory structure just in case, though volume handles it
RUN mkdir -p /app/storage/uploads

CMD ["python", "app.py"]
