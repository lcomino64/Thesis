FROM debian:stable-slim

# Install required packages including Python
RUN apt-get update && \
    apt-get install -y \
    nmap \
    ncat \
    openssl \
    python3 \
    python3-pip \
    && pip3 install tqdm --break-system-packages \
    && rm -rf /var/lib/apt/lists/*

COPY client.py /app/client.py
COPY generate_testfiles.sh /app/generate_testfiles.sh
RUN chmod +x /app/generate_testfiles.sh
RUN chmod +x /app/client.py

# Create a startup script
COPY startup.sh /app/startup.sh
RUN chmod +x /app/startup.sh

WORKDIR /app

ENTRYPOINT ["/app/startup.sh"]
