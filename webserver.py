from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import requests
# from django.http import HttpResponse
from yookassa.domain.notification import WebhookNotification
from flask import Flask, request
import ssl

class handler(BaseHTTPRequestHandler):
    print("line 9")
    def do_GET(self):
        print("do_GET")
        self.send_response(200)
        self.send_header('Content-type','text/html')
        self.end_headers()
        message = "Lobanova senior-pomidor!!!11"
        self.wfile.write(bytes(message, "utf8"))

    def do_POST(self):
        print("do_POST")
        self.send_response(200)
        self.send_header('Content-type','text/html')
        self.end_headers()
        length = int(self.headers.get('content-length'))
        message = json.loads(self.rfile.read(length))
        self.wfile.write(bytes(json.dumps(message), "utf8"))
        print (message)     

httpd = HTTPServer(('', 443), handler)
print("HTTPServer")


httpd.socket = ssl.wrap_socket (httpd.socket,
        keyfile="/etc/letsencrypt/live/lobanova.ml/privkey.pem",
        certfile='/etc/letsencrypt/live/lobanova.ml/fullchain.pem', server_side=True)
httpd.serve_forever()   

# with HTTPServer(('', 443), handler) as server:
#     print("HTTPServer")
#     server.serve_forever()


