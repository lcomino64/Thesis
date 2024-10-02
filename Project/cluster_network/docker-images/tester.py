import os
import time
import json
import sqlite3
from contextlib import closing
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
import requests
from datetime import datetime
import random


# Raspberry Pi IPs
PI_IPS = ["192.168.1.11", "192.168.1.12", "192.168.1.13", "192.168.1.14"]
BOARD_IP = "192.168.1.50"
TESTER_IP = "192.168.1.100"


class MetricsHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers["Content-Length"])
        post_data = self.rfile.read(content_length)
        metrics = json.loads(post_data.decode("utf-8"))

        if "server_metrics" in metrics:
            self.server.store_server_metrics(metrics["server_metrics"])
        elif "client_metrics" in metrics:
            self.server.store_client_metrics(metrics["client_metrics"])

        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"OK")

    def log_message(self, format, *args):
        # Suppress logging
        return


class MetricsServer(HTTPServer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.db_conn = None
        self.db_path = None

    def set_database(self, db_path):
        if self.db_conn:
            self.db_conn.close()
        self.db_path = db_path
        self.db_conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self.setup_database()

    def setup_database(self):
        with closing(self.db_conn.cursor()) as cursor:
            cursor.execute(
                """CREATE TABLE IF NOT EXISTS server_metrics
                            (timestamp REAL, cpu_usage REAL, memory_usage REAL, 
                            active_clients INTEGER, total_bytes_processed INTEGER, 
                            bytes_processed_per_second INTEGER, temperature REAL)"""
            )

            cursor.execute(
                """CREATE TABLE IF NOT EXISTS client_metrics
                            (file_size INTEGER, operation TEXT, start_time REAL, 
                            end_time REAL, total_time REAL, queue_time REAL, 
                            network_time REAL, processing_time REAL, total_sent INTEGER, 
                            total_received INTEGER, operation_completed BOOLEAN)"""
            )
        self.db_conn.commit()

    def store_server_metrics(self, metrics):
        with closing(self.db_conn.cursor()) as cursor:
            cursor.execute(
                """INSERT INTO server_metrics VALUES 
                            (?, ?, ?, ?, ?, ?, ?)""",
                (
                    metrics["timestamp"],
                    metrics["cpu_usage"],
                    metrics["memory_usage"],
                    metrics["active_clients"],
                    metrics["total_bytes_processed"],
                    metrics["bytes_processed_per_second"],
                    metrics["temperature"],
                ),
            )
        self.db_conn.commit()

    def store_client_metrics(self, metrics):
        with closing(self.db_conn.cursor()) as cursor:
            cursor.execute(
                """INSERT INTO client_metrics VALUES 
                            (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (
                    metrics["file_size"],
                    metrics["operation"],
                    metrics["start_time"],
                    metrics["end_time"],
                    metrics["total_time"],
                    metrics["queue_time"],
                    metrics["network_time"],
                    metrics["processing_time"],
                    metrics["total_sent"],
                    metrics["total_received"],
                    metrics["operation_completed"],
                ),
            )
        self.db_conn.commit()


def start_metrics_server():
    metrics_port = 8000
    server = MetricsServer((TESTER_IP, metrics_port), MetricsHandler)
    metrics_thread = threading.Thread(target=server.serve_forever)
    metrics_thread.daemon = True
    metrics_thread.start()
    return server


def create_new_database(configuration, test_name):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    db_name = f"{configuration}_{test_name}_{timestamp}.db"
    os.makedirs("data", exist_ok=True)
    return os.path.join("data", db_name)


def run_test(
    server,
    configuration,
    test_name,
    num_clients,
    file_path,
    operation,
    max_duration=300,
):
    print(
        f"Starting test: {test_name} - {num_clients} clients, file: {file_path}, operation: {operation} for configuration: {configuration}"
    )

    # Create a new database for this test
    db_path = create_new_database(configuration, test_name)
    server.set_database(db_path)

    # Calculate clients per Pi
    clients_per_pi = num_clients // len(PI_IPS)
    remainder = num_clients % len(PI_IPS)

    completion_urls = []
    # Send commands to Raspberry Pis
    for i, pi_ip in enumerate(PI_IPS):
        clients = clients_per_pi + (1 if i < remainder else 0)
        if clients > 0:
            command = {
                "test_name": test_name,
                "filename": file_path,
                "operation": operation,
                "num_clients": clients,
            }
            try:
                response = requests.post(
                    f"http://{pi_ip}:8080", json=command, timeout=10
                )
                response.raise_for_status()
                start_status = response.json()
                print(
                    f"Command sent to Pi {pi_ip}: {clients} clients. Status: {start_status['status']}"
                )

                # Get completion URL from header
                completion_url = response.headers.get("X-Completion-URL")
                if completion_url:
                    print(f"Completion URL for Pi {pi_ip}: {completion_url}")
                    completion_urls.append(completion_url)
                else:
                    print(f"No completion URL provided for Pi {pi_ip}")
            except requests.RequestException as e:
                print(f"Error communicating with Pi {pi_ip}: {str(e)}")

    # Poll completion URLs until all are complete or max duration is reached
    start_time = time.time()
    completed_clients = set()
    while (
        len(completed_clients) < len(completion_urls)
        and time.time() - start_time < max_duration
    ):
        for i, url in enumerate(completion_urls):
            if i not in completed_clients:
                try:
                    completion_response = requests.get(url, timeout=10)
                    if completion_response.status_code == 200:
                        completion_status = completion_response.json()
                        print(
                            f"Pi {i+1} completed. Status: {completion_status['status']}"
                        )
                        if completion_status["status"] == "failed":
                            print(f"Error message: {completion_status['message']}")
                        completed_clients.add(i)
                    elif (
                        completion_response.status_code != 404
                    ):  # 404 means not completed yet
                        print(
                            f"Unexpected status code {completion_response.status_code} from Pi {i+1}"
                        )
                except requests.RequestException as e:
                    print(f"Error checking completion status for Pi {i+1}: {str(e)}")
        if len(completed_clients) < len(completion_urls):
            time.sleep(1)  # Wait 1 second before polling again

    if len(completed_clients) < len(completion_urls):
        print(
            f"Warning: Not all clients completed within the maximum duration of {max_duration} seconds"
        )

    print(f"Test {test_name} completed.")
    return db_path


def run_large_scale_test(
    server,
    configuration,
    total_clients,
    file_sizes,
    operation,
    max_duration=3600,
    chunk_size=50,
):
    test_name = f"large_scale_{total_clients}_clients"
    print(
        f"Starting large scale test: {test_name} - {total_clients} clients, file sizes: {file_sizes}, operation: {operation}"
    )

    db_path = create_new_database(configuration, test_name)
    server.set_database(db_path)

    start_time = time.time()
    total_completed = 0
    chunk_number = 0

    while total_completed < total_clients and time.time() - start_time < max_duration:
        chunk_number += 1
        chunk_clients = min(chunk_size, total_clients - total_completed)
        print(f"Starting chunk {chunk_number} with {chunk_clients} clients")

        clients_per_pi = chunk_clients // len(PI_IPS)
        remainder = chunk_clients % len(PI_IPS)

        completion_urls = []
        for i, pi_ip in enumerate(PI_IPS):
            clients = clients_per_pi + (1 if i < remainder else 0)
            if clients > 0:
                command = {
                    "test_name": f"{test_name}_chunk_{chunk_number}",
                    "filename": random.choice(file_sizes),
                    "operation": operation,
                    "num_clients": clients,
                }
                try:
                    response = requests.post(
                        f"http://{pi_ip}:8080", json=command, timeout=10
                    )
                    response.raise_for_status()
                    start_status = response.json()
                    print(
                        f"Command sent to Pi {pi_ip}: {clients} clients. Status: {start_status['status']}"
                    )

                    completion_url = response.headers.get("X-Completion-URL")
                    if completion_url:
                        print(f"Completion URL for Pi {pi_ip}: {completion_url}")
                        completion_urls.append(completion_url)
                    else:
                        print(f"No completion URL provided for Pi {pi_ip}")
                except requests.RequestException as e:
                    print(f"Error communicating with Pi {pi_ip}: {str(e)}")

        # Wait for chunk completion
        chunk_completed = 0
        chunk_start_time = time.time()
        while (
            chunk_completed < len(completion_urls)
            and time.time() - chunk_start_time < 600
        ):  # 10 minutes timeout per chunk
            for url in completion_urls:
                try:
                    completion_response = requests.get(url, timeout=10)
                    if completion_response.status_code == 200:
                        chunk_completed += 1
                        completion_urls.remove(url)
                except requests.RequestException:
                    pass
            time.sleep(5)

        total_completed += chunk_clients
        print(
            f"Chunk {chunk_number} completed. Total clients completed: {total_completed}/{total_clients}"
        )

        # Add a delay between chunks to allow system to stabilize
        time.sleep(1)

    total_time = time.time() - start_time
    print(
        f"Large scale test completed in {total_time:.2f} seconds. Total clients completed: {total_completed}/{total_clients}"
    )
    return db_path


# def run_drowning_rate_test(
#     server,
#     configuration,
#     duration=3600,
#     initial_rate=50,
#     rate_increase=0,
#     chunk_size=50,
# ):
#     test_name = f"drowning_rate_{duration}s"
#     print(f"Starting drowning rate test: {test_name} - Duration: {duration} seconds")

#     db_path = create_new_database(configuration, test_name)
#     server.set_database(db_path)

#     node_ip = "192.168.64.8"  # Hardcoded IP address

#     file_sizes = [
#         "client/test_files/10mb.txt",
#         "client/test_files/50mb.txt",
#         "client/test_files/100mb.txt",
#     ]
#     client_pods = v1.list_namespaced_pod(
#         namespace="default", label_selector="app=client"
#     )

#     start_time = time.time()
#     current_rate = initial_rate
#     total_clients = 0
#     chunk_number = 0

#     while time.time() - start_time < duration:
#         chunk_number += 1
#         chunk_clients = min(int(current_rate), chunk_size)
#         print(
#             f"Starting chunk {chunk_number} with {chunk_clients} clients (current rate: {current_rate:.2f} clients/s)"
#         )

#         clients_per_pod = chunk_clients // len(client_pods.items)
#         remainder = chunk_clients % len(client_pods.items)

#         completion_urls = []
#         for i in range(len(client_pods.items)):
#             clients = clients_per_pod + (1 if i < remainder else 0)
#             if clients > 0:
#                 command = {
#                     "test_name": f"{test_name}_chunk_{chunk_number}",
#                     "filename": random.choice(file_sizes),
#                     "operation": "encrypt",
#                     "num_clients": clients,
#                 }
#                 try:
#                     response = requests.post(
#                         f"http://{node_ip}:30080", json=command, timeout=10
#                     )
#                     response.raise_for_status()
#                     start_status = response.json()
#                     print(
#                         f"Command sent to client {i+1}: {clients} clients. Status: {start_status['status']}"
#                     )

#                     completion_url = response.headers.get("X-Completion-URL")
#                     if completion_url:
#                         completion_url = completion_url.replace(
#                             "localhost", node_ip
#                         ).replace("8081", "30081")
#                         completion_urls.append(completion_url)
#                     else:
#                         print(f"No completion URL provided for client {i+1}")
#                 except requests.RequestException as e:
#                     print(f"Error communicating with client {i+1}: {str(e)}")

#         total_clients += chunk_clients

#         # Wait for chunk completion or timeout
#         chunk_completed = 0
#         chunk_start_time = time.time()
#         while (
#             chunk_completed < len(completion_urls)
#             and time.time() - chunk_start_time < 300
#         ):  # 5 minutes timeout per chunk
#             for url in completion_urls[:]:
#                 try:
#                     completion_response = requests.get(url, timeout=10)
#                     if completion_response.status_code == 200:
#                         chunk_completed += 1
#                         completion_urls.remove(url)
#                 except requests.RequestException:
#                     pass
#             time.sleep(1)

#         print(f"Chunk {chunk_number} completed. Total clients so far: {total_clients}")

#         # Increase the rate
#         current_rate += rate_increase

#         # Add a small delay between chunks to allow system to stabilize
#         time.sleep(1)

#     total_time = time.time() - start_time
#     print(
#         f"Drowning rate test completed in {total_time:.2f} seconds. Total clients: {total_clients}"
#     )
#     return db_path


def run_basic_test_1(server, configuration):
    return run_test(
        server,
        configuration,
        "basic_1",
        1,
        "client/test_files/2mb.txt",
        "encrypt",
        max_duration=600,
    )


def run_basic_test_2(server, configuration):
    return run_test(
        server,
        configuration,
        "basic_2",
        10,
        "client/test_files/2mb.txt",
        "encrypt",
        max_duration=1200,
    )


def run_basic_test_3(server, configuration):
    return run_test(
        server,
        configuration,
        "basic_3",
        20,
        "client/test_files/2mb.txt",
        "encrypt",
        max_duration=1200,
    )


def run_all_basic_tests(server, configuration):
    db_paths = []
    # db_paths.append(run_basic_test_1(server, configuration))
    time.sleep(1)  # Add a small delay between tests
    db_paths.append(run_basic_test_2(server, configuration))
    time.sleep(1)  # Add a small delay between tests
    # db_paths.append(run_basic_test_3(server, configuration))
    return db_paths


def run_1000_client_tests(server, configuration):
    file_sizes = [
        "client/test_files/10mb.txt",
        "client/test_files/50mb.txt",
        "client/test_files/100mb.txt",
    ]
    db_paths = []
    for file_size in file_sizes:
        db_path = run_large_scale_test(
            server,
            configuration,
            1000,
            [file_size],
            "encrypt",
            max_duration=7200,
            chunk_size=50,
        )
        db_paths.append(db_path)
        time.sleep(1)  # Add a longer delay between tests
    return db_paths


def view_database_contents(db_path):
    conn = sqlite3.connect(db_path)
    with closing(conn.cursor()) as cursor:
        print("\nServer Metrics:")
        cursor.execute("SELECT * FROM server_metrics LIMIT 5")
        print(cursor.fetchall())

        print("\nClient Metrics:")
        cursor.execute("SELECT * FROM client_metrics LIMIT 5")
        print(cursor.fetchall())

    print("\nMetrics Summary:")
    with closing(conn.cursor()) as cursor:
        cursor.execute("SELECT COUNT(*) FROM server_metrics")
        server_count = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM client_metrics")
        client_count = cursor.fetchone()[0]

    print(f"Total server metrics collected: {server_count}")
    print(f"Total client metrics collected: {client_count}")


def main():
    server = start_metrics_server()

    print("Running basic tests...")
    basic_db_paths = run_all_basic_tests(server, "raspberry-pi")

    # print("\nRunning 1000 client tests...")
    # large_scale_db_paths = run_1000_client_tests(server, "raspberry-pi")

    # print("\nRunning drowning rate test...")
    # drowning_rate_db_path = run_drowning_rate_test(
    #     server,
    #     "raspberry-pi",
    #     duration=3600,
    #     initial_rate=1,
    #     rate_increase=0.1,
    #     chunk_size=50,
    # )

    all_db_paths = basic_db_paths  # + large_scale_db_paths + [drowning_rate_db_path]

    print("\n=== Viewing results of all tests ===")
    for db_path in all_db_paths:
        print(f"\nViewing contents of {db_path}:")
        view_database_contents(db_path)


if __name__ == "__main__":
    main()
