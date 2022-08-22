from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from django.http import HttpResponse
from yookassa.domain.notification import WebhookNotification
from flask import Flask, request

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type','text/html')
        self.end_headers()

        message = "Lobanova senior-pomidor!!!11"
        self.wfile.write(bytes(message, "utf8"))

    def do_POST(self):
        self.send_response(200)
        self.send_header('Content-type','text/html')
        self.end_headers()
        message = "POST response"
        # event_json = json.loads(request.body)
        # body_unicode = request.body.decode('utf-8')
        # body = json.loads(body_unicode)
        # content = body['content']
        self.wfile.write(bytes(message, "utf8"))
        
@app.route('/post_json', methods=['POST'])
    def process_json():
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        json = request.json
        return json
    else:
        return 'Content-Type not supported!'
        # try:
        #     print("notification_object")
        #     notification_object = WebhookNotification(event_json)
        # except Exception:
        #     message = "POST response error"
    
        # payment = notification_object.object
        # message2 = payment
        # self.wfile.write(bytes(message2, "utf8"))

# def my_webhook_handler(request):
#     event_json = json.loads(request.body)
#     return HttpResponse(status=200)

# # Cоздайте объект класса уведомлений в зависимости от события
# try:
#     notification_object = WebhookNotification(event_json)
# except Exception as e:
#     # обработка ошибок
#     print(repr(e))
#     print("notification_object error")

# # Получите объекта платежа
# payment = notification_object.object

#         # Cоздайте объект класса уведомлений в зависимости от события
# try:
#     print("notification_object")
#     notification_object = WebhookNotification(event_json)
# except Exception:
#     print("notification_object error")
#     # обработка ошибок

#     # Получите объекта платежа
# payment = notification_object.object

with HTTPServer(('', 443), handler) as server:
    server.serve_forever()
