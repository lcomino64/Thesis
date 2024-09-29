FROM debian:stable-slim

# Install required packages including Python
RUN apt-get update && \
    apt-get install -y \
    nmap \
    ncat \
    openssl \
    python3 \
    python3-pip \
    && pip3 install tqdm requests --break-system-packages \
    && rm -rf /var/lib/apt/lists/*

COPY client.py /app/client.py
COPY generate_testfiles.sh /app/generate_testfiles.sh
RUN chmod +x /app/generate_testfiles.sh
RUN chmod +x /app/client.py

# Create a startup script
COPY startup.sh /app/startup.sh
RUN chmod +x /app/startup.sh

# Create a wait-for-command script
COPY wait-for-command.py /app/wait-for-command.py
RUN chmod +x /app/wait-for-command.py

WORKDIR /app

ENTRYPOINT ["/app/startup.sh"]