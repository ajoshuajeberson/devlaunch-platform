from http.server import BaseHTTPRequestHandler, HTTPServer
import json


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/health":
            response = {"status": "healthy"}
            status = 200
        elif self.path == "/":
            response = {
                "application": "DevLaunch Sample API",
                "version": "1.0.0",
                "platform": "DevLaunch",
            }
            status = 200
        else:
            response = {"error": "Not found"}
            status = 404

        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(response).encode())

    def log_message(self, format, *args):
        print(f"{self.client_address[0]} - {format % args}")


if __name__ == "__main__":
    server = HTTPServer(("0.0.0.0", 8000), Handler)
    print("DevLaunch Sample API listening on port 8000")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down DevLaunch Sample API")
        server.server_close()
