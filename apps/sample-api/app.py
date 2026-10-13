from http.server import BaseHTTPRequestHandler, HTTPServer
import json


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/health":
            response = {"status": "healthy"}
            self.send_response(200)
        elif self.path == "/":
            response = {
                "application": "DevLaunch Sample API",
                "version": "1.0.0",
                "platform": "DevLaunch"
            }
            self.send_response(200)
        else:
            response = {"error": "Not found"}
            self.send_response(404)

        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(response).encode())

    def log_message(self, format, *args):
        print(f"{self.client_address[0]} - {format % args}")


server = HTTPServer(("0.0.0.0", 8000), Handler)
print("DevLaunch Sample API listening on port 8000")
server.serve_forever()
