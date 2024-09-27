FROM debian:stable-slim

# Install required packages including Python
RUN apt-get update && \
    apt-get install -y \
    nmap \
    ncat \
    openssl \
    python3 \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

COPY client.py /app/client.py
RUN chmod +x /app/client.py

# Set the command to run your Python script
CMD ["python3", "/app/client.py"]
