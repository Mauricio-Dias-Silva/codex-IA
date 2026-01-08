# Base Image
FROM python:3.11-slim

# Working Directory
WORKDIR /app

# Install System Dependencies (for Flet/Canvas if needed)
# Flet usually doesn't need much, but git is useful only if we clone inside
RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

# Copy Requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy App Source
COPY . .

# Environment Variables
ENV PORT=8080
ENV FLET_SERVER_PORT=8080
ENV PYTHONUNBUFFERED=1

# Expose Port
EXPOSE 8080

# Command to Run
CMD ["python", "web_entrypoint.py"]
