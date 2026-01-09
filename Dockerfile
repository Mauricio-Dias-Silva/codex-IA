FROM python:3.11

WORKDIR /app

# Install system dependencies for Google GenAI / Grpcio
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    software-properties-common \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy App Code
COPY . .

# Environment Defaults
ENV PORT=8080

# Run Streamlit
CMD streamlit run web_app.py --server.port=$PORT --server.address=0.0.0.0 --server.headless=true
