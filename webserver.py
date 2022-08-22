from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from django.http import HttpResponse
from yookassa.domain.notification import WebhookNotification

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
        event_json = json.loads(request.body)
        self.wfile.write(bytes(message, "utf8"))
        # try:
        #     print("notification_object")
        #     notification_object = WebhookNotification(event_json)
        # except Exception:
        #     message = "POST response error"
    
        # payment = notification_object.object
        # message2 = payment
        # self.wfile.write(bytes(message2, "utf8"))
        
def my_webhook_handler(request):
    event_json = json.loads(request.body)
    return HttpResponse(status=200)

# Cоздайте объект класса уведомлений в зависимости от события
try:
    notification_object = WebhookNotification(event_json)
except Exception:
    # обработка ошибок

# Получите объекта платежа
payment = notification_object.object

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
