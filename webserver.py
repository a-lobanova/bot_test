from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import requests
# from django.http import HttpResponse
from yookassa.domain.notification import WebhookNotification
from flask import Flask, request
import ssl
import socket
import certifi

import os

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

hostname = 'lobanova.ml:443'
PROTOCOL_TLS_CLIENT requires valid cert chain and hostname
context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
context.load_verify_locations('/etc/letsencrypt/live/lobanova.ml/fullchain.pem')

with socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0) as sock:
    with context.wrap_socket(sock, server_hostname= "") as ssock:
        print("ssock.version()", ssock.version())

# httpd.socket = ssl.SSLContext.wrap_socket(httpd.socket,
#         keyfile="/etc/letsencrypt/live/lobanova.ml/privkey.pem",
#         certfile='/etc/letsencrypt/live/lobanova.ml/fullchain.pem', server_side=True)
# httpd.socket = ssl.wrap_socket (httpd.socket,
#         keyfile="/etc/letsencrypt/live/lobanova.ml/privkey.pem",
#         certfile='/etc/letsencrypt/live/lobanova.ml/fullchain.pem', server_side=True)

# Create a place holder to consolidate SSL settings

# i.e., Create an SSLContext

# contextInstance                 = ssl.SSLContext();

# contextInstance.verify_mode     = ssl.CERT_REQUIRED;

 

# # Load the CA certificates used for validating the peer's certificate

# contextInstance.load_verify_locations("/etc/letsencrypt/live/lobanova.ml/fullchain.pem");

 

# # Create a client socket

# socketInstance = socket.socket();

 

# # Get an instance of SSLSocket

# sslSocketInstance  = contextInstance.wrap_socket(socketInstance);

 

# print(type(sslSocketInstance));

 

# # Connect to a server

# sslSocketInstance.connect(("", 443));

 

# print("Version of the SSL Protocol:%s"%sslSocketInstance.version());

# print("Cipher used:");

# print(sslSocketInstance.cipher());

httpd.serve_forever()   

# with HTTPServer(('', 443), handler) as server:
#     print("HTTPServer")
#     server.serve_forever()


