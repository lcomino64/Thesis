FROM debian:stable-slim

RUN apt-get update && \
    apt-get install -y \
    python3 \
    python3-pip \
    openssl \
    sqlite3 \
    && pip3 install tqdm requests \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY client.py /app/client.py
COPY generate_testfiles.sh /app/generate_testfiles.sh
COPY tester.py /app/tester.py
COPY requirements.txt /app/requirements.txt

RUN pip3 install -r requirements.txt

RUN chmod +x /app/generate_testfiles.sh /app/client.py /app/tester.py

CMD ["python3", "/app/tester.py"]