from http.server import BaseHTTPRequestHandler, HTTPServer

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type','text/html')
        self.end_headers()

        message = "Lobanova senior-pomidor!!!11"
        self.wfile.write(bytes(message, "utf8"))

with HTTPServer(('', 443), handler) as server:
    server.serve_forever()
