from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import requests
from django.http import HttpResponse
from yookassa.domain.notification import WebhookNotification
from flask import Flask, request
import ssl
import socket
import certifi
# import var_dump as var_dump
from yookassa import Webhook
from yookassa.domain.notification import WebhookNotificationEventType
# from multiprocessing import Pool

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
        self.send_header('Content-type','application/json')
        self.end_headers()
        length = int(self.headers.get('content-length'))
        message = json.loads(self.rfile.read(length))
        print (message)    

    # def my_webhook_handler(request):
    #     print("my_webhook_handler(request):")
    #     event_json = json.loads(request.body)
    #     try:
    #         # Создание объекта класса уведомлений в зависимости от события
    #         notification_object = WebhookNotificationFactory().create(event_json)
    #         response_object = notification_object.object
    #         if notification_object.event == WebhookNotificationEventType.PAYMENT_SUCCEEDED:
    #             some_data = {
    #                 'paymentId': response_object.id,
    #                 'paymentStatus': response_object.status,
    #             }
    #             # Специфичная логика
    #             # ...
    #         elif notification_object.event == WebhookNotificationEventType.PAYMENT_WAITING_FOR_CAPTURE:
    #             some_data = {
    #                 'paymentId': response_object.id,
    #                 'paymentStatus': response_object.status,
    #             }
    #     except Exception:
    #     # Обработка ошибок
    #         print("# Сообщаем кассе об ошибке")
    #         return HttpResponse(status=400)  # Сообщаем кассе об ошибке
    #     return HttpResponse(status=200)


httpd = HTTPServer(('', 80), handler)
# httpd.socket = ssl.wrap_socket(
#     httpd.socket, 
#     certfile='/etc/letsencrypt/live/lobanova.ml/fullchain.pem', 
#     keyfile = '/etc/letsencrypt/live/lobanova.ml/privkey.key',  
#     ssl_version=ssl.PROTOCOL_TLS,
#     server_side=True)
httpd.serve_forever()

