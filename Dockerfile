# Dockerfile

# 1. Base image
FROM python:3.10-slim

# 2. Set working dir and copy source
WORKDIR /app
COPY . /app

# 3. Install system deps (if any), then Python deps
RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential \
    && pip install --no-cache-dir -r requirements.txt \
    && apt-get purge -y build-essential \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# 4. Expose Django port
EXPOSE 8000

# 5. Default command for FastAPI/Django runserver
#    (override in docker-compose for migrations if needed)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
