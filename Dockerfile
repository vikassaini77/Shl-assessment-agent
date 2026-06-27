FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY . .

# Expose port (Render sets PORT env variable automatically, usually 10000 but we can map it)
ENV PORT=8000
EXPOSE 8000

# Run Uvicorn without reload
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
