import socket
import os
from tqdm import tqdm
import argparse
import time
import requests
import json
import threading


CHUNK_SIZE = 1048576  # 64 KB, must match server's CHUNK_SIZE


def verify_operation(filename, output_filename, operation):
    if operation == "encrypt":
        # For encryption, check if output file size is within expected range
        original_size = os.path.getsize(filename)
        encrypted_size = os.path.getsize(output_filename)

        # Encrypted file should be slightly larger due to padding, but not more than 1% larger
        return original_size <= encrypted_size <= original_size * 1.01
    else:  # decrypt
        # For decryption, compare first 1KB of decrypted file with original
        with open(filename[:-4], "rb") as original, open(
            output_filename, "rb"
        ) as decrypted:
            original_start = original.read(1024)
            decrypted_start = decrypted.read(1024)
        return original_start == decrypted_start


def send_file(filename, operation, metrics_url):
    host = "192.168.1.50"
    port = 8080

    operation_completed = False

    print(f"Checking file: {filename}")
    if not os.path.exists(filename):
        print(f"Error: File {filename} does not exist!")
        return

    file_size = os.path.getsize(filename)
    print(f"File size: {file_size} bytes")
    output_filename = f"{filename}.enc" if operation == "encrypt" else filename[:-4]

    print(f"Connecting to {host}:{port}")
    start_time = time.time()
    network_start_time = start_time

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 4 * CHUNK_SIZE)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 4 * CHUNK_SIZE)

        s.connect((host, port))
        network_time = time.time() - network_start_time

        print(
            f"Connected. Sending operation byte: {'0' if operation == 'encrypt' else '1'}"
        )
        s.sendall(b"\x00" if operation == "encrypt" else b"\x01")

        print("Waiting for acknowledgement")
        queue_start = time.time()
        ack = s.recv(20)
        if ack == b"OK":
            print("Received acknowledgement: {ack}")

            queue_end = time.time()
            queue_time = queue_end - queue_start
        elif ack == b"QUEUED":
            print("Server busy, request queued")
            while True:
                ack = s.recv(2)
                if ack == b"OK":
                    print("Received acknowledgement: OK")
                    queue_end = time.time()
                    queue_time = queue_end - queue_start
                    break
                time.sleep(1)

        elif ack == b"MAX_CLIENTS_REACHED":
            print("Server has reached maximum client capacity. Try again later.")
            return  # or implement a retry mechanism
        else:
            print("Did not receive correct acknowledgement from server")
            return

        total_sent = 0
        total_received = 0

        print(f"Opening file: {filename}")
        try:
            with open(filename, "rb") as f:
                print("File opened successfully")
                with open(output_filename, "wb") as out_f:
                    with tqdm(
                        total=file_size, unit="B", unit_scale=True, desc="Sending"
                    ) as pbar_send, tqdm(
                        total=None, unit="B", unit_scale=True, desc="Receiving"
                    ) as pbar_recv:

                        while True:
                            chunk = f.read(CHUNK_SIZE)
                            if not chunk:
                                print("Finished reading file")
                                break
                            chunk_size = len(chunk)
                            print(f"Read chunk of size: {chunk_size}")
                            print(f"Sending chunk size: {chunk_size}")

                            chunk_send_start = time.time()
                            s.sendall(chunk_size.to_bytes(4, byteorder="big"))
                            print(f"Sending chunk of {chunk_size} bytes")
                            s.sendall(chunk)
                            chunk_send_end = time.time()

                            network_time += chunk_send_end - chunk_send_start

                            total_sent += chunk_size
                            pbar_send.update(chunk_size)

                            print("Waiting for processed chunk size")

                            chunk_recv_start = time.time()
                            size_data = s.recv(4)
                            if not size_data:
                                print("Server closed connection")
                                break
                            chunk_size = int.from_bytes(size_data, byteorder="big")
                            if chunk_size == 0:
                                print("Server reported an error processing the chunk")
                                break
                            print(f"Receiving processed chunk of {chunk_size} bytes")

                            processed_chunk = b""
                            while len(processed_chunk) < chunk_size:
                                data = s.recv(chunk_size - len(processed_chunk))
                                if not data:
                                    print("Server closed connection unexpectedly")
                                    break
                                processed_chunk += data

                            chunk_recv_end = time.time()
                            network_time += chunk_recv_end - chunk_recv_start

                            out_f.write(processed_chunk)
                            total_received += len(processed_chunk)
                            pbar_recv.update(len(processed_chunk))

            if total_sent == file_size and total_received:
                operation_completed = True

        except IOError as e:
            print(f"Error opening or reading file: {e}")
            return

    end_time = time.time()
    total_time = end_time - start_time
    processing_time = total_time - network_time

    output_filename = f"{filename}.enc" if operation == "encrypt" else filename[:-4]

    operation_completed = verify_operation(filename, output_filename, operation)

    client_metrics = {
        "client_metrics": {
            "file_size": file_size,
            "operation": operation,
            "start_time": start_time,
            "end_time": end_time,
            "total_time": total_time,
            "queue_time": queue_time,
            "network_time": network_time,
            "processing_time": processing_time,
            "total_sent": total_sent,
            "total_received": total_received,
            "operation_completed": operation_completed,
        }
    }

    print(f"CLIENT_METRICS: {json.dumps(client_metrics)}")

    # Send metrics to the HTTP server
    try:
        response = requests.post(metrics_url, json=client_metrics)
        if response.status_code == 200:
            print("Metrics successfully sent to the server")
        else:
            print(f"Failed to send metrics. Status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Error sending metrics to server: {e}")

    print(f"\nProcessed file saved as {output_filename}")
    print(f"Total sent: {total_sent} bytes, Total received: {total_received} bytes")


def client_thread(file_path, operation, metrics_url):
    send_file(file_path, operation, metrics_url)


def run_clients(num_clients, file_path, operation, metrics_url):
    threads = []
    for _ in range(num_clients):
        thread = threading.Thread(
            target=client_thread, args=(file_path, operation, metrics_url)
        )
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()


def main():
    parser = argparse.ArgumentParser(
        description="Client for file encryption/decryption"
    )
    parser.add_argument("filename", help="Path to the file to be processed")
    parser.add_argument(
        "operation", choices=["encrypt", "decrypt"], help="Operation to perform"
    )
    parser.add_argument(
        "--metrics-url",
        default=os.environ.get("METRICS_URL", "http://192.168.1.100:8000/metrics"),
        help="URL to send metrics to",
    )
    parser.add_argument(
        "--num-clients", type=int, default=1, help="Number of client threads to run"
    )

    args = parser.parse_args()

    run_clients(args.num_clients, args.filename, args.operation, args.metrics_url)


if __name__ == "__main__":
    main()
