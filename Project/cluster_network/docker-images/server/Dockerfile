FROM debian:stable-slim

# Install required packages including Python
RUN apt-get update && \
    apt-get install -y \
    nmap \
    ncat \
    openssl \
    python3 \
    python3-pip \
    && pip3 install psutil requests --break-system-packages \
    && rm -rf /var/lib/apt/lists/*

COPY server.py /app/server.py
RUN chmod +x /app/server.py

# Set the command to run your Python script
CMD ["python3", "/app/server.py"]
