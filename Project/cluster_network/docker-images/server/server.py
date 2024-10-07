import socket
import subprocess
import threading
from threading import Thread
import time
import psutil
import json
from queue import Queue
import mmap
import struct


def get_temperature():
    CSR_BASE = 0xF0000000
    XADC_BASE = CSR_BASE + 0x9000

    XADC_TEMP_OFFSET = 0x00

    with open("/dev/mem", "r+b") as f:
        mem = mmap.mmap(f.fileno(), 4096, offset=XADC_BASE)

        mem.seek(XADC_TEMP_OFFSET)
        temp_raw = struct.unpack("<I", mem.read(4))[0]

        mem.close()

    return (temp_raw / 4095) * 165 - 40


CHUNK_SIZE = 1048576  # 1 MB, adjust if needed
MAX_CLIENTS = 10

# Global variables for tracking metrics
total_bytes_processed = 0
active_clients = 0
client_lock = threading.Lock()
bytes_processed_last_second = 0

client_queue = Queue()
active_threads = []
client_event = threading.Event()


def parse_url(url):
    # Simple URL parsing
    protocol, rest = url.split("://", 1)
    host_port, path = rest.split("/", 1) if "/" in rest else (rest, "")
    host, port = host_port.split(":") if ":" in host_port else (host_port, "80")
    return host, int(port), "/" + path


def send_metrics_to_server(metrics_url):
    global total_bytes_processed, active_clients, bytes_processed_last_second
    last_total_bytes = 0

    host, port, path = parse_url(metrics_url)

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
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((host, port))

                json_data = json.dumps(server_metrics)
                request = f"POST {path} HTTP/1.1\r\n"
                request += f"Host: {host}\r\n"
                request += "Content-Type: application/json\r\n"
                request += f"Content-Length: {len(json_data)}\r\n"
                request += "\r\n"
                request += json_data

                s.sendall(request.encode())

                response = s.recv(1024).decode()
                status_line = response.split("\r\n")[0]
                status_code = int(status_line.split()[1])

                if status_code != 200:
                    print(f"Failed to send metrics. Status code: {status_code}")

        except Exception as e:
            print(f"Error sending metrics to server: {e}")

        time.sleep(0.1)  # Log every second


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


def process_queued_clients():
    global active_clients

    while True:
        client_event.wait()  # Wait for a client to be added or processed
        client_event.clear()

        with client_lock:
            while client_queue.qsize() > 0 and active_clients < MAX_CLIENTS:
                conn, addr = client_queue.get()
                active_clients += 1
                print(
                    f"Processing queued client from {addr}. Active clients: {active_clients}"
                )
                threading.Thread(target=process_client, args=(conn, addr)).start()


def process_client(conn, addr):
    global total_bytes_processed, active_clients

    print(f"New connection from {addr}")
    conn.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
    conn.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 4 * CHUNK_SIZE)
    conn.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 4 * CHUNK_SIZE)

    start_time = time.time()

    print(f"[{addr}] Waiting for operation byte")
    op_byte = conn.recv(1)
    operation = "encrypt" if op_byte == b"\x00" else "decrypt"
    print(f"[{addr}] Operation: {operation}")

    try:
        print(f"[{addr}] Sending acknowledgement")
        conn.sendall(b"OK")

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

        print(f"[{addr}] Client operation completed")

    finally:
        conn.close()
        with client_lock:
            active_clients -= 1
            print(f"Connection closed. Active clients: {active_clients}")
        client_event.set()  # Notify that a client has finished processing

        end_time = time.time()
        duration = end_time - start_time

        print(
            f"Connection from {addr} closed. Total processed: {total_bytes_processed} bytes, Duration: {duration:.2f} seconds"
        )


def handle_client(conn, addr):
    global active_clients

    with client_lock:
        if active_clients < MAX_CLIENTS:
            active_clients += 1
            print(f"New connection accepted. Active clients: {active_clients}")
            threading.Thread(target=process_client, args=(conn, addr)).start()
        else:
            print(f"Max clients reached. Queueing connection from {addr}")
            client_queue.put((conn, addr))
            conn.sendall(b"QUEUED")

    client_event.set()


def main():
    host = "0.0.0.0"
    port = 8080
    metrics_url = "http://192.168.1.100:8000/metrics"

    # Start the metrics sending thread
    metrics_thread = threading.Thread(
        target=send_metrics_to_server, args=(metrics_url,), daemon=True
    )
    metrics_thread.start()

    queue_thread = threading.Thread(target=process_queued_clients, daemon=True)
    queue_thread.start()

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((host, port))
        s.listen()
        print(f"Server listening on {host}:{port}")
        while True:
            conn, addr = s.accept()
            handle_client(conn, addr)


if __name__ == "__main__":
    main()
