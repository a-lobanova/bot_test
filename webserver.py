from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import requests
from django.http import HttpResponse
from yookassa.domain.notification import WebhookNotification
from flask import Flask, request

# class handler(BaseHTTPRequestHandler):
#     def do_GET(self):
#         self.send_response(200)
#         self.send_header('Content-type','text/html')
#         self.end_headers()

#         message = "Lobanova senior-pomidor!!!11"
#         self.wfile.write(bytes(message, "utf8"))

#     def do_POST(self):
#         self.send_response(200)
#         self.send_header('Content-type','text/html')
#         self.end_headers()
#         message = "POST response"
#         self.wfile.write(bytes(message, "utf8"))
#         content_type = request.headers.get('Content-Type')
#         try:    
#             print("try")
#             json = request.json
#             return json
#         except:
#             return print('Content-Type not supported!')
        

# with HTTPServer(('', 443), handler) as server:
#     server.serve_forever()


app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hello!'

@app.route('/post_json', methods=['POST'])
def process_json():
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        json = request.json
        return json
    else:
        return 'Content-Type not supported!'

if __name__ == '__ws__':
    app.run(host='0.0.0.0', port=443, debug=True)
