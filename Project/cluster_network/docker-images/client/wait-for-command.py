import http.server
import socketserver
import json
import subprocess
import concurrent.futures
import threading
import uuid

PORT = 8080
COMPLETION_PORT = 8081

# Dictionary to store completion statuses
completion_statuses = {}
PI_IPS = ["192.168.1.11", "192.168.1.12", "192.168.1.13", "192.168.1.14"]


class CommandHandler(http.server.SimpleHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers["Content-Length"])
        post_data = self.rfile.read(content_length)
        command = json.loads(post_data.decode("utf-8"))

        print(f"Received command: {command}")

        if (
            "filename" in command
            and "operation" in command
            and "num_clients" in command
        ):
            # Generate a unique ID for this command
            command_id = str(uuid.uuid4())

            # Send immediate confirmation with completion URL
            self.send_response(202)  # 202 Accepted
            self.send_header("Content-type", "application/json")
            self.send_header(
                "X-Completion-URL", f"http://{PI_IPS[0]}:{COMPLETION_PORT}/{command_id}"
            )
            self.end_headers()
            self.wfile.write(
                json.dumps({"status": "started", "id": command_id}).encode()
            )

            # Start client processes in parallel
            threading.Thread(
                target=self.run_client_processes, args=(command, command_id)
            ).start()
        else:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b"Invalid command format")

    def run_client_processes(self, command, command_id):
        num_clients = int(command["num_clients"])

        with concurrent.futures.ThreadPoolExecutor(max_workers=num_clients) as executor:
            futures = [
                executor.submit(self.run_client_process, command)
                for _ in range(num_clients)
            ]
            concurrent.futures.wait(futures)

        # Aggregate results
        results = [future.result() for future in futures]
        overall_status = (
            "completed"
            if all(result["status"] == "completed" for result in results)
            else "failed"
        )
        overall_message = "\n".join(result["message"] for result in results)

        # Store completion status
        completion_statuses[command_id] = {
            "status": overall_status,
            "message": overall_message,
        }

    def run_client_process(self, command):
        try:
            result = subprocess.run(
                [
                    "python3",
                    "client/client.py",
                    command["filename"],
                    command["operation"],
                    "--num-clients",
                    "1",  # Each subprocess handles one client
                ],
                check=True,
                capture_output=True,
                text=True,
            )
            return {"status": "completed", "message": "Command executed successfully"}
        except subprocess.CalledProcessError as e:
            return {
                "status": "failed",
                "message": f"Error executing command: {str(e)}\nStderr: {e.stderr}",
            }


class CompletionHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        command_id = self.path[1:]  # Remove leading '/'
        if command_id in completion_statuses:
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(completion_statuses[command_id]).encode())
            del completion_statuses[command_id]  # Clean up after sending
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"Completion status not found")


def run_command_server():
    with socketserver.TCPServer(("", PORT), CommandHandler) as httpd:
        print(f"Command server running on port {PORT}")
        httpd.serve_forever()


def run_completion_server():
    with socketserver.TCPServer(("", COMPLETION_PORT), CompletionHandler) as httpd:
        print(f"Completion server running on port {COMPLETION_PORT}")
        httpd.serve_forever()


if __name__ == "__main__":
    command_thread = threading.Thread(target=run_command_server)
    completion_thread = threading.Thread(target=run_completion_server)

    command_thread.start()
    completion_thread.start()

    command_thread.join()
    completion_thread.join()
