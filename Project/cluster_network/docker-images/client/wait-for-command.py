import http.server
import socketserver
import json
import subprocess

PORT = 8080


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
            try:
                subprocess.run(
                    [
                        "python3",
                        "/app/client.py",
                        command["filename"],
                        command["operation"],
                        "--num-clients",
                        str(command["num_clients"]),
                    ],
                    check=True,
                )
                self.send_response(200)
                self.end_headers()
                self.wfile.write(b"Command executed successfully")
            except subprocess.CalledProcessError as e:
                self.send_response(500)
                self.end_headers()
                self.wfile.write(f"Error executing command: {str(e)}".encode())
        else:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b"Invalid command format")


with socketserver.TCPServer(("", PORT), CommandHandler) as httpd:
    print(f"Serving at port {PORT}")
    httpd.serve_forever()
