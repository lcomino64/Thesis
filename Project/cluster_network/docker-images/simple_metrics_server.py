from http.server import HTTPServer, BaseHTTPRequestHandler
import json


class MetricsHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers["Content-Length"])
        post_data = self.rfile.read(content_length)
        metrics = json.loads(post_data.decode("utf-8"))

        print("Received metrics:")
        print(json.dumps(metrics, indent=2))

        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"OK")


def run_server(port=8000):
    server_address = ("", port)
    httpd = HTTPServer(server_address, MetricsHandler)
    print(f"Metrics server running on port {port}")
    httpd.serve_forever()


if __name__ == "__main__":
    run_server()
