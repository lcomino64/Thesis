import os
import time
import json
from kubernetes import client, config
import sqlite3
from contextlib import closing
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
import requests

# Load the Kubernetes configuration
kubeconfig = os.environ.get("KUBECONFIG", "~/.kube/config")
config.load_kube_config(config_file=kubeconfig)

v1 = client.CoreV1Api()
apps_v1 = client.AppsV1Api()


def get_service_url(service_name, namespace="default"):
    try:
        service = v1.read_namespaced_service(service_name, namespace)
        if service.spec.type == "NodePort":
            nodes = v1.list_node()
            node_ip = nodes.items[0].status.addresses[0].address
            node_port = next(
                port.node_port for port in service.spec.ports if port.port == 8080
            )
            return f"http://{node_ip}:{node_port}"
        else:
            return f"http://{service.spec.cluster_ip}:{service.spec.ports[0].port}"
    except client.exceptions.ApiException:
        print(f"Service {service_name} not found in namespace {namespace}")
        return None


# Metrics server
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
        self.db_conn = sqlite3.connect("metrics.db", check_same_thread=False)
        self.setup_database()

    def setup_database(self):
        with closing(self.db_conn.cursor()) as cursor:
            cursor.execute(
                """CREATE TABLE IF NOT EXISTS server_metrics
                            (timestamp REAL, cpu_usage REAL, memory_usage REAL, 
                            active_clients INTEGER, total_bytes_processed INTEGER, 
                            bytes_processed_per_second INTEGER)"""
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
                            (?, ?, ?, ?, ?, ?)""",
                (
                    metrics["timestamp"],
                    metrics["cpu_usage"],
                    metrics["memory_usage"],
                    metrics["active_clients"],
                    metrics["total_bytes_processed"],
                    metrics["bytes_processed_per_second"],
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


def run_metrics_server(port):
    server = MetricsServer(("0.0.0.0", port), MetricsHandler)
    print(f"Metrics server running on all interfaces, port {port}")
    server.serve_forever()


def run_test(num_clients, file_path, operation, duration=5):
    print(
        f"Starting test: {num_clients} clients, file: {file_path}, operation: {operation}"
    )

    client_service_url = get_service_url("client-service")
    if not client_service_url:
        print("Failed to get client service URL")
        return

    # Calculate clients per pod
    client_pods = v1.list_namespaced_pod(
        namespace="default", label_selector="app=client"
    )
    clients_per_pod = num_clients // len(client_pods.items)
    remainder = num_clients % len(client_pods.items)

    # Send commands to client pods
    for i in range(len(client_pods.items)):
        clients = clients_per_pod + (1 if i < remainder else 0)
        if clients > 0:
            command = {
                "filename": file_path,
                "operation": operation,
                "num_clients": clients,
            }
            try:
                response = requests.post(
                    f"{client_service_url}", json=command, timeout=10
                )
                response.raise_for_status()
                print(f"Command sent to client {i+1}: {clients} clients")
            except requests.RequestException as e:
                print(f"Error sending command to client {i+1}: {str(e)}")

    # Wait for the test duration
    time.sleep(duration)

    print("Test completed.")


def run_basic_tests():
    file_sizes = [10, 50, 100]  # mb
    client_counts = [10, 50, 100]
    operation = "encrypt"

    print(f"\n{'='*50}")
    print(f"Running test with 1 client, 1gb file")
    print(f"{'='*50}\n")

    file_path = f"/app/test_files/1gb.txt"
    run_test(1, file_path, operation)
    time.sleep(5)  # Add a small delay between tests

    for num_clients in client_counts:
        size = file_sizes[1]
        file_path = f"/app/test_files/{size}mb.txt"

        print(f"\n{'='*50}")
        print(f"Running test with {num_clients} clients, {size}mb file")
        print(f"{'='*50}\n")
        run_test(num_clients, file_path, operation)
        time.sleep(5)  # Add a small delay between tests


def view_database_contents():
    conn = sqlite3.connect("metrics.db")
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
    # Start metrics server in a separate thread
    metrics_port = 8000
    metrics_thread = threading.Thread(target=run_metrics_server, args=(metrics_port,))
    metrics_thread.daemon = True
    metrics_thread.start()

    # Run tests
    run_basic_tests()

    # View database contents
    view_database_contents()


if __name__ == "__main__":
    main()
