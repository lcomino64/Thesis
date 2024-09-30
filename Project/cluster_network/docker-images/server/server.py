import socket
import subprocess
import threading
import time
import psutil
import json
import requests
import os

import mmap
import struct

def get_temperature():
    CSR_BASE = 0xf0000000
    XADC_BASE = CSR_BASE + 0x9000

    XADC_TEMP_OFFSET = 0x00  

    with open("/dev/mem", "r+b") as f:
        mem = mmap.mmap(f.fileno(), 4096, offset=XADC_BASE)

        mem.seek(XADC_TEMP_OFFSET)
        temp_raw = struct.unpack("<I", mem.read(4))[0]

        mem.close()

    return (temp_raw / 4095) * 165 - 40


CHUNK_SIZE = 1048576  # 1 MB, adjust if needed

# Global variables for tracking metrics
total_bytes_processed = 0
active_clients = 0
bytes_processed_last_second = 0


def send_metrics_to_server(metrics_url):
    global total_bytes_processed, active_clients, bytes_processed_last_second
    last_total_bytes = 0
    while True:
        current_time = time.time()
        cpu_usage = psutil.cpu_percent()
        memory_usage = psutil.virtual_memory().percent
        temperature = get_temperature()

        # Calculate bytes processed in the last second
        bytes_processed_last_second = total_bytes_processed - last_total_bytes
        last_total_bytes = total_bytes_processed

        server_metrics = {
            "server_metrics": {
                "timestamp": current_time,
                "cpu_usage": cpu_usage,
                "memory_usage": memory_usage,
                "active_clients": active_clients,
                "total_bytes_processed": total_bytes_processed,
                "bytes_processed_per_second": bytes_processed_last_second,
                "temperature": temperature,
            }
        }

        print(f"SERVER_METRICS: {json.dumps(server_metrics)}")

        try:
            response = requests.post(metrics_url, json=server_metrics)
            if response.status_code != 200:
                print(f"Failed to send metrics. Status code: {response.status_code}")
                pass
        except requests.exceptions.RequestException as e:
            print(f"Error sending metrics to server: {e}")
            pass

        time.sleep(1)  # Log every second


def process_data(data, operation, is_last_chunk):
    key = "00" * 16
    iv = "00" * 16

    if operation == "encrypt":
        cmd = ["openssl", "enc", "-aes-128-cbc", "-K", key, "-iv", iv, "-nosalt"]
        if not is_last_chunk:
            cmd.append("-nopad")
    else:  # decrypt
        cmd = ["openssl", "enc", "-d", "-aes-128-cbc", "-K", key, "-iv", iv, "-nosalt"]
        if not is_last_chunk:
            cmd.append("-nopad")

    p = subprocess.Popen(
        cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    stdout, stderr = p.communicate(input=data)

    if p.returncode != 0:
        raise Exception(f"OpenSSL error: {stderr.decode()}")

    return stdout


def handle_client(conn, addr):
    global total_bytes_processed, active_clients

    print(f"New connection from {addr}")
    conn.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
    conn.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 4 * CHUNK_SIZE)
    conn.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 4 * CHUNK_SIZE)

    start_time = time.time()
    active_clients += 1

    print(f"[{addr}] Waiting for operation byte")
    op_byte = conn.recv(1)
    operation = "encrypt" if op_byte == b"\x00" else "decrypt"
    print(f"[{addr}] Operation: {operation}")

    print(f"[{addr}] Sending acknowledgement")
    conn.sendall(b"OK")

    try:
        while True:
            print(f"[{addr}] Waiting for chunk size")
            size_data = conn.recv(4)
            if not size_data:
                print(f"[{addr}] Client closed connection")
                break
            chunk_size = int.from_bytes(size_data, byteorder="big")
            print(f"[{addr}] Expecting chunk of {chunk_size} bytes")

            chunk = b""
            while len(chunk) < chunk_size:
                data = conn.recv(chunk_size - len(chunk))
                if not data:
                    print(f"[{addr}] Client closed connection unexpectedly")
                    return
                chunk += data

            if not chunk:
                print(f"[{addr}] Received empty chunk, closing connection")
                break

            total_bytes_processed += len(chunk)
            print(
                f"Received chunk of {len(chunk)} bytes from {addr}. Total processed: {total_bytes_processed} bytes"
            )

            try:
                is_last_chunk = chunk_size < CHUNK_SIZE
                processed_chunk = process_data(chunk, operation, is_last_chunk)
                print(f"[{addr}] Processed chunk, size: {len(processed_chunk)} bytes")
                conn.sendall(len(processed_chunk).to_bytes(4, byteorder="big"))
                conn.sendall(processed_chunk)
            except Exception as e:
                print(f"[{addr}] Error processing chunk: {e}")
                conn.sendall(
                    (0).to_bytes(4, byteorder="big")
                )  # Send 0 to indicate error
                break

    finally:
        conn.close()

        end_time = time.time()
        duration = end_time - start_time
        active_clients -= 1

        print(
            f"Connection from {addr} closed. Total processed: {total_bytes_processed} bytes, Duration: {duration:.2f} seconds"
        )


def main():
    host = "0.0.0.0"
    port = 8080
    metrics_url = "http://192.168.1.100:8000/metrics"


    # Start the metrics sending thread
    metrics_thread = threading.Thread(
        target=send_metrics_to_server, args=(metrics_url,), daemon=True
    )
    metrics_thread.start()

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((host, port))
        s.listen()
        print(f"Server listening on {host}:{port}")
        while True:
            conn, addr = s.accept()
            client_thread = threading.Thread(target=handle_client, args=(conn, addr))
            client_thread.start()


if __name__ == "__main__":
    main()