FROM python:3.12-slim

WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy only requirements first to leverage Docker cache
COPY db/setup.py db/setup.py
COPY utils/setup.py utils/setup.py
COPY bot/setup.py bot/setup.py

# Install dependencies
RUN pip install --no-cache-dir \
    -e db \
    -e utils \
    -e bot

# Copy the rest of the application
COPY . .

# Set Python path
ENV PYTHONPATH=/app

CMD ["python", "-m", "bot.src.main"]