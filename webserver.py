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
httpd.socket = ssl.wrap_socket (httpd.socket, certfile='/etc/letsencrypt/live/lobanova.ml/fullchain.pem', keyfile = '/etc/letsencrypt/live/lobanova.ml/privkey.pem',  server_side=True)
httpd.serve_forever()

# print("HTTPServer")

# hostname = 'lobanova.ml'
# # PROTOCOL_TLS_CLIENT requires valid cert chain and hostname
# context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
# context.load_verify_locations('/etc/letsencrypt/live/lobanova.ml/fullchain6.pem')

# with socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0) as sock:
#     with context.wrap_socket(sock, server_hostname= hostname) as ssock:
#         print("ssock.version()", ssock.version())

# context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
# context.load_cert_chain('/etc/letsencrypt/live/lobanova.ml/fullchain.pem', '/etc/letsencrypt/live/lobanova.ml/privkey.pem')

# with socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0) as sock:
#     print("socket.socket")
#     sock.bind(('', 443))
#     sock.listen(5)
#     with context.wrap_socket(sock, server_side=True) as ssock:
#         conn, addr = ssock.accept()
#         print("ssock.version()", ssock.version())

# with context.wrap_socket(sock, server_side=True) as ssock:
#     conn, addr = ssock.accept()
#     print("ssock.version()", ssock.version())




# # IP address and port number

# ipAddress   = "";

# portNumber  = 443;

# # SSLContext construction

# sslSettings                     = ssl.SSLContext();

# sslSettings.verify_mode         = ssl.CERT_REQUIRED;

 

# # Load a CA certificate.

# # The CA certificate The will be used to validate the certificate from the server

# sslSettings.load_verify_locations("/etc/letsencrypt/live/lobanova.ml/fullchain.pem");

 

# # Loading of client certificate which will be validated by the server

# sslSettings.load_cert_chain(certfile="/etc/letsencrypt/live/lobanova.ml/fullchain.pem", keyfile="/etc/letsencrypt/live/lobanova.ml/privkey.key");

 

# # Streaming socket

# s = socket.socket();

 

# # Obtain SSLSocket instance

# ss  = sslSettings.wrap_socket(s);

 

# # Get rid of the original socket

# s.close();

 

# # Connect to the server

# ss.connect((ipAddress, portNumber));

 

# # Print the loaded certificate statistics

# print("Certificates currently loaded into the SSLContext");

# print(sslSettings.cert_store_stats());

 

# # Send a message to the server

# ss.sendall("Hello Server!".encode());

 

# # Receive time from server

# dataFromServer = ss.recv(1024);

 

# print("Message received from the server");

# print(dataFromServer);   

  

# # Close the secure socket

# ss.close();   

# httpd = HTTPServer(('', 443), handler)
# print("HTTPServer")


