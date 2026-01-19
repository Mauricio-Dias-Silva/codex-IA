FROM python:3.11-slim

WORKDIR /app

# Install dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PORT=8080
ENV FLET_SERVER_PORT=8080

# Run Flet App (Web Mode)
CMD ["flet", "run", "--web", "--port", "8080", "--headless", "codex_gui.py"]
