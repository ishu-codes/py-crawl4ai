FROM python:3.13-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install uv
RUN uv venv
RUN sh .venv/bin/activate
RUN uv pip install --upgrade pip
RUN uv pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .

EXPOSE 8000

CMD ["sh", "-c", ". .venv/bin/activate && fastapi dev main.py --host 0.0.0.0 --port 8000"]

