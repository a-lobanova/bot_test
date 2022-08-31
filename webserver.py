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
        self.send_header('Content-type','multipart/form-data')
        self.end_headers()
        message = "Lobanova senior-pomidor!!!11"
        self.wfile.write(bytes(message, "utf8"))

    def do_POST(self):
        print("do_POST")
        self.send_response(200)
        self.send_header('Content-type','application/json')
        self.end_headers()
        length = int(self.headers.get('content-length'))
        message = json.loads(self.rfile.read(length))
        self.wfile.write(bytes(json.dumps(message), "utf8"))
        print (message)     


httpd = HTTPServer(('', 443), handler)
httpd.socket = ssl.wrap_socket(
    httpd.socket, 
    certfile='/etc/letsencrypt/live/lobanova.ml/fullchain.pem', 
    keyfile = '/etc/letsencrypt/live/lobanova.ml/privkey.key',  
    ssl_version=ssl.PROTOCOL_TLS,
    server_side=True)
httpd.serve_forever()

