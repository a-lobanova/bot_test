import logging
import telebot

import asyncio
import re
import yookassa
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types.message import ContentTypes
import markups as nav
from db import Database
from config import Config
from const import Const
# import error_handler

import requests

import xlsxwriter
import uuid
from yookassa import Configuration, Payment, Webhook, Settings
import var_dump as var_dump
from multiprocessing import Process

import json
from django.http import HttpResponse
from yookassa.domain.notification import WebhookNotification
# import tracemalloc

# tracemalloc.start()


config = Config
const = Const

# data = requests.get('https://www.cbr-xml-daily.ru/daily_json.js').json()
data = requests.get('https://www.tinkoff.ru/api/v1/currency_rates/').json()
rate = (data['payload']['rates'][72]['sell'])
print(rate)

TOKEN = config.token
    
logging.basicConfig(level = logging.INFO)

bot = Bot(token = TOKEN)

dp = Dispatcher(bot)

db = Database('database.db')

adminId = config.adminId

Configuration.account_id = config.Configuration_account_id
Configuration.secret_key = config.Configuration_secret_key

Configuration.configure_auth_token(config.access_token)

settings = Settings.get_account_settings()
print(settings)

# params = {'limit': 2}
# res1 = Payment.list(params)
# print('res1', res1)
# var_dump.var_dump(Payment.list(params))


# response = Webhook.add({
#     "event": "payment.succeeded",
#     "url": "https://lobanova.net/payment/yookassa",
# })

# response = Webhook.add({
#     "event": "payment.waiting_for_capture",
#     "url": "https://lobanova.net/payment/yookassa",
# })

# response = Webhook.add({
#     "event": "payment.canceled",
#     "url": "https://lobanova.net/payment/yookassa",
# })

# list = Webhook.list()
# print("webhook list", list)
# var_dump.var_dump(Webhook.list())


from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from django.http import HttpResponse
import ssl
import socket
import certifi
import os

class handler(BaseHTTPRequestHandler):
    print("class handler")
    def do_GET(self):
        try:
            print("do_GET")
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b'Lobanova senior-pomidor!!!11')
        except Exception as e:
            print("error do_GET", repr(e))

    def do_POST(self):
        print("do_POST")
        self.send_response(200)
        self.send_header('Content-type','application/json')
        self.end_headers()
        length = int(self.headers.get('content-length'))
        message = json.loads(self.rfile.read(length))
        print(message)
        status = (message['event'])
        order_id_raw = (message['object']['description'])
        f = filter(str.isdecimal, order_id_raw)
        order_id = "".join(f)
        if status == "payment.succeeded":
            # Уведомление об успешном платеже за заказ 
            if db.get_orderStatus(order_id) == "wait payment":
                db.set_orderStatus(order_id, "complitedPayment")
                db.set_update(order_id) 
                user_id = db.get_user_id_through_order_id(order_id)
                order_inform = "Заказ оплачен через ЮКасса!\n" + "Пользователь: " + db.get_nickname(user_id) + db.get_paid_order_through_order_id(order_id) 
                print(order_inform)
                # remove inline buttons
                asyncio.run(bot.edit_message_text(chat_id=adminId, message_id=db.get_message_id(order_id), 
                    text = "Получена оплата за заказ #" + order_id))
                asyncio.run(bot.send_message(user_id, "Платеж принят!"))
                asyncio.run(bot.send_message(adminId, order_inform, reply_markup=nav.orderRedeemedMurkup(order_id)))
            # Уведомление об успешном платеже за Доставку 
            elif db.get_orderStatus(order_id) == "wait delivery payment":
                db.set_orderStatus(order_id, "paidOrderDelivery")
                db.set_update(order_id) 
                user_id = db.get_user_id_through_order_id(order_id)
                order_inform = "Доставка оплачена через ЮКасса!\n" + "Пользователь: " + db.get_nickname(user_id) + db.get_delivery_paid_order_through_order_id(order_id)  
                    # remove inline buttons
                asyncio.run(bot.edit_message_text(chat_id=adminId, message_id=db.get_message_id(order_id), 
                    text = "Получена оплата за ДОСТАВКУ заказа #" + order_id))
                asyncio.run(bot.send_message(user_id, "Платеж за доставку принят!"))
                asyncio.run(bot.send_message(adminId, order_inform, reply_markup=nav.sentOrderMurkup(order_id)))


httpd = HTTPServer(('', 443), handler)
httpd.socket = ssl.wrap_socket(
    httpd.socket, 
    certfile='/etc/letsencrypt/live/lobanova.net/fullchain.pem', 
    keyfile = '/etc/letsencrypt/live/lobanova.net/privkey.pem',  
    ssl_version=ssl.PROTOCOL_TLS,
    server_side=True)

def payment(value, description):
    payment = Payment.create({
    "amount": {
        "value": value,
        "currency": "RUB"
    },
    "payment_method_data": {
        "type": "bank_card"
    },
    "confirmation": {
        "type": "redirect",
        "return_url": "www.lobanova.net"
    },
    "capture": True,
    "description": description
    }, uuid.uuid4())

    return json.loads(payment.json())

def dataOutput(records, text):
    answer = f"Все заказы за промежуток времени - {text}\n"
    for r in records:
        answer += f" 📦Номер заказа - {r[0]}\n"
        answer += f" 👤Клиент - {db.get_nickname(r[1])}\n"
        answer += f" Наименование - {r[2]}\n"
        answer += f" Дата заказа {r[3]}\n"
        answer += f" Статус - {r[5]}\n"
        answer += f" Дата обновления {r[10]}\n"
    return(answer)

def orderIdFromMessege(text):
    s = text
    result = re.findall("Номер заказа - \d+", s)
    mystr = ' '.join(map(str,result))
    number_result = [int(number_result) for number_result in str.split(mystr) if number_result.isdigit()]
    return(number_result)  

def report(text):
    interval = text
    records = db.get_all_orders_in_time(interval)
    if(records):
        answer = dataOutput(records, interval)
        markup = nav.changeMarkup()
    else:
        answer = "Записей не обнаружено!"
        markup = None
    return[answer, markup]

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    #sti = open('static/welcome.tgs', 'rb')
    #await bot.send_sticker(message.chat.id, sti)
    if (message.from_user.id == adminId):
        await bot.send_message(message.from_user.id, "Admin", reply_markup = nav.mainMenuAdmin)

    else:

        if (not db.user_exists(message.from_user.id)):
            print("not user_exists")
            db.add_user(message.from_user.id)
            await bot.send_message(message.from_user.id, "Добро пожаловать, рада Bас приветствовать! Я - бот созданный чтобы принимать заказы. Для регистарции укажите ФИО")
        else:
            print("user_exists")
            await bot.send_message(message.from_user.id, "Добро пожаловать, " + db.get_nickname(message.from_id) + " рада Bас приветствовать! Я - бот созданный чтобы принимать заказы. Вы уже зарегистрированы.", reply_markup=nav.mainMenu)


@dp.message_handler(content_types=['text'])
async def bot_message(message: types.Message):
    if message.from_id != adminId:
        userId = message.from_id
        if message.chat.type == 'private':
            if message.text == 'Профиль/Мои заказы':
                user_nickname = "Ваше ФИО: " + db.get_nickname(userId) + "\nНомер телефона: " + db.get_contact(userId)
                records = db.get_orders(userId)
                if(records):
                    answer = f"🕘 История Заказов\n"
                    for r in records:
                        answer += f" {r[2]}\n"
                        answer += f" {r[3]}\n"
                        answer += f"Статус заказа: {r[5]}\n"
                    await bot.send_message(userId, answer)
                else:
                    await message.reply("Записей не обнаружено!")
                await bot.send_message(userId, user_nickname)

            elif message.text == 'Создать заказ':
                await bot.send_message(userId, "Введите заказ: бренд, наименование, размер, цвет, количество")
                db.set_signup(userId, "set_order")
            else:
                if db.get_signup(userId) == "setnickname":
                    if (len(message.text)>60):
                        await bot.send_message(userId, "not more then 60 carrecters")
                    elif '@' in message.text or '/' in message.text or ';' in message.text or '*' in message.text:
                        await bot.send_message(userId, "incorrect symbol")
                    else:
                        db.set_nickname(userId, message.text)
                        db.set_signup(userId, "set_number")
                        await bot.send_message(userId, "ФИО записано, введите номер своего телефона, нажав на кнопку ниже", reply_markup=nav.getContac)
                elif db.get_signup(userId) == "set_order":
                     db.add_order(userId, message.text)
                     await bot.send_message(userId, "Заказ записан, ожидайте подтверждения" + db.get_lastOrder(userId))
                     db.set_signup(userId, "make order")
                     order_id = db.get_lastOrder_id(userId)
                     order_inform = "Пользователь: " + db.get_nickname(userId) + "\nTелефон: " + db.get_contact(userId) + "\nСделал заказ " + db.get_lastOrder(userId)
                     await bot.send_message(adminId, order_inform, reply_markup = nav.createMarkup(order_id))
                else:
                    await bot.send_message(userId, "Ошибка🤷‍♀️ Выберете действие", reply_markup=nav.mainMenu)
    else:
        if (db.order_status_exists("wait price")):
            print("buyer_message 1")
            order_id = db.get_order_id("wait price")
            user_id = db.get_user_id_through_order_id(order_id)
            try:
                a = int(message.text)
                db.set_price(order_id, message.text)
                db.set_orderStatus(order_id, "wait payment")
                summa = round((int(message.text) + 50) * rate)
                await bot.send_message(user_id, "Заказ подтвержден." + "\nНомер заказа - " + str(order_id) +"\nСумма к оплате, включая комисиию(50EUR): " + str(summa) + " руб. По курсу Тинькофф 1EUR = " + str(rate), reply_markup = nav.paymentMarkup(order_id))
                await bot.send_message(adminId, "Уведомление об оплате отправлено пользователю: " + str(summa) + "руб.")
                db.set_rubprice(order_id, summa)
            except Exception as e:
                print(repr(e))
                await message.reply("Ожидается ввод суммы")
                print("else", message.text)
        elif(db.order_status_exists("orderRedeemed")):
            print("buyer_message 2 delivery")
            order_id = db.get_order_id("orderRedeemed")
            user_id = db.get_user_id_through_order_id(order_id)
            try:
                a = int(message.text)
                db.set_delivery_price(order_id, message.text)
                db.set_orderStatus(order_id, "wait delivery payment")
                summa = round((int(message.text)) * rate)
                await bot.send_message(user_id, "Сумма доставки " + str(summa) + " руб. По курсу Тинькофф 1EUR = " + str(rate) + "\nНомер заказа - " + str(order_id), reply_markup = nav.deliveryPaymentMarkup(order_id))
                await bot.send_message(adminId, "Уведомление об оплате за ДОСТАВКУ отправлено пользователю: " + str(summa) + "руб.")
                db.set_deliveryrubprice(order_id, summa)
            except Exception as e:
                print(repr(e))
                await message.reply("Ожидается ввод суммы")

        elif message.text == 'Все заказы':
                await bot.send_message(adminId, "Выберите интервал времени", reply_markup = nav.allOrdersMarkup())
        elif message.text == const.day:
            answer = report(const.day)[0]
            markup = report(const.day)[1]
            await bot.send_message(adminId, answer, reply_markup = markup)
        elif message.text == const.week:
            answer = report(const.week)[0]
            markup = report(const.week)[1]
            await bot.send_message(adminId, answer, reply_markup = markup)
        elif message.text == const.twoWeeks:
            answer = report(const.twoWeeks)[0]
            markup = report(const.twoWeeks)[1]
            await bot.send_message(adminId, answer, reply_markup = markup)
        elif message.text == const.month:
            answer = report(const.month)[0]
            markup = report(const.month)[1]
            await bot.send_message(adminId, answer, reply_markup = markup)
        elif message.text == "Все время":
                records = db.get_all_orders_in_time("all")
                if(records):
                    row = 1
                    col = 0
                    answer = dataOutput(records, message.text)
                    workbook = xlsxwriter.Workbook('Report.xlsx')
                    worksheet = workbook.add_worksheet()
                    for r in records:
                        worksheet.write('A1', 'Номер заказа')
                        worksheet.write('B1', 'Клиент')
                        worksheet.write('C1', 'Наименование')
                        worksheet.write('D1', 'Дата заказа')
                        worksheet.write('E1', 'Цена заказа в евро')
                        worksheet.write('F1', 'Статус заказа')
                        worksheet.write('G1', 'Дата обновления')
                        worksheet.write(row, col, r[0]) 
                        worksheet.write(row, col + 1, db.get_nickname(r[1]))
                        worksheet.write(row, col+2, r[2]) 
                        worksheet.write(row, col + 3, r[3]) 
                        worksheet.write(row, col + 4, r[4]) 
                        worksheet.write(row, col+5, r[5]) 
                        worksheet.write(row, col + 6, r[10])
                        row += 1
                    workbook.close()
                    await bot.send_message(adminId, answer, reply_markup = nav.changeMarkup())
                    await bot.send_document(adminId, document=open('Report.xlsx', 'rb'))
                else:
                    await message.reply("Записей не обнаружено!")
        elif message.text == "❌ Отмена":
            await bot.send_message(adminId, "Выберете действие", reply_markup=nav.mainMenuAdmin)

@dp.message_handler(content_types=['contact'])
async def bot_contact (message):
    print(message)
    userId = message.from_id
    if message.chat.type == 'private':
        if db.get_signup(userId) == "set_number":
                    db.set_contact(userId, message.contact.phone_number)
                    db.set_signup(userId, "done")
                    await bot.send_message(userId, "Регистрация прошла успешно, теперь вы будете получать все данные о заказе через бота", reply_markup=nav.mainMenu)
    else:
        await bot.send_message(userId, "Ошибка🤷‍♀️\n" + "Выберете действие", reply_markup=nav.mainMenu)

@dp.callback_query_handler(text = "bankDetails")
async def callback_inline(call: types.CallbackQuery):
    await bot.send_message(call.message.chat.id, config.bank_details)
    await bot.send_photo(call.message.chat.id, photo=open('static/qr.jpg', 'rb'))

@dp.callback_query_handler(text = "UKassa")
async def callback_inline(call: types.CallbackQuery):
    orderId = str(orderIdFromMessege(call.message.text))
    f = filter(str.isdecimal, orderId)
    order_id = "".join(f)
    print("UKassa type(order_id)",type(order_id))
    if db.get_orderStatus(order_id) == "wait payment":
        print("db.get_orderStatus(order_id) == wait payment")
        # amount = str(round(db.get_rubprice(order_id)))+"00"
        amount = str(round(db.get_rubprice(order_id)))
        amountPrice = int(amount)
        description = ("Заказ №", order_id)
        payment_deatils = payment(amount, description)
        await bot.send_message(chat_id = call.from_user.id, text = (payment_deatils['confirmation'])['confirmation_url'] )
        # await bot.send_invoice(chat_id = call.from_user.id, title = "Оплата заказа #" + order_id, description = description, payload = order_id, provider_token = config.UKassaTestToken,
            # currency = "RUB", start_parameter = "test_bot", prices=[{"label":"Руб", "amount": amountPrice}])
        print("payment_deatils", payment_deatils)

    elif db.get_orderStatus(order_id) == "wait delivery payment":
        print("db.get_orderStatus(order_id) == wait delivery payment")
        amount = str(round(db.get_deliveryrubprice(order_id)))+"00"
        amountPrice = int(amount)
        description = db.get_orderDesc(order_id)
        await bot.send_invoice(chat_id = call.from_user.id, title = "Оплата ДОСТАВКИ заказа #" + order_id, description = description, payload = order_id, provider_token = config.UKassaTestToken,
            currency = "RUB", start_parameter = "test_bot", prices=[{"label":"Руб", "amount": amountPrice}])
    else:
        await bot.send_message(call.from_user.id, "Ошибка🤷‍♀️\n Возможно, оплата уже произведена.")       

# @dp.pre_checkout_query_handler()
# async def process_pre_chechout_query(pre_checkout_query: types.PreCheckoutQuery):
#     print("process_pre_chechout_query \n", pre_checkout_query)
#     await bot.answer_pre_checkout_query(pre_checkout_query.id, ok = True)


# @dp.message_handler(content_types=ContentTypes.SUCCESSFUL_PAYMENT)
# async def process_pay(message: types.Message):
#     order_id = message.successful_payment.invoice_payload
#     print("message \n", message)
#     if db.order_exists(message.successful_payment.invoice_payload):
#         # Уведомление об успешном платеже за заказ 
#         if db.get_orderStatus(order_id) == "wait payment":
#             db.set_orderStatus(order_id, "complitedPayment")
#             db.set_update(order_id) 
#             user_id = db.get_user_id_through_order_id(order_id)
#             order_inform = "Заказ оплачен через ЮКасса!\n" + "Пользователь: " + db.get_nickname(user_id) + db.get_paid_order_through_order_id(order_id) 
#             # remove inline buttons
#             # print("db.get_message_id(order_id)", db.get_message_id(order_id))
#             await bot.edit_message_text(chat_id=adminId, message_id=db.get_message_id(order_id), text = "Получена оплата за заказ #" + order_id)
#             await bot.send_message(message.from_user.id, "Платеж принят!")
#             await bot.send_message(adminId, order_inform, reply_markup=nav.orderRedeemedMurkup(order_id))
#         # Уведомление об успешном платеже за Доставку 
#         elif db.get_orderStatus(order_id) == "wait delivery payment":
#             db.set_orderStatus(order_id, "paidOrderDelivery")
#             db.set_update(order_id) 
#             user_id = db.get_user_id_through_order_id(order_id)
#             order_inform = "Доставка оплачена через ЮКасса!\n" + "Пользователь: " + db.get_nickname(user_id) + db.get_delivery_paid_order_through_order_id(order_id)  
#                 # remove inline buttons
#             await bot.edit_message_text(chat_id=adminId, message_id=db.get_message_id(order_id), text = "Получена оплата за ДОСТАВКУ заказа #" + order_id)
#             await bot.send_message(message.from_user.id, "Платеж за доставку принят!")
#             await bot.send_message(adminId, order_inform, reply_markup=nav.sentOrderMurkup(order_id))

@dp.callback_query_handler()
async def callback_inline(call):
    try:
        if call.message:
            if call.data:
                # print("call", call)
                if "ok" in call.data:
                    print ("Подтвердить")
                    okOrderId = call.data.partition("ok")[2]
                    db.set_update(okOrderId)
                    print("type(okOrderId)", type(okOrderId))
                        # remove inline buttons
                    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text = call.message.text + f'\nЗаказ подтвержден, введите сумму в евро к оплате. Курс на сегодня 1EUR = {rate} руб.',
                        reply_markup=None)
                    db.set_orderStatus(okOrderId, "wait price") 
                elif "cancel" in call.data:
                    print ("Отменить заказ")
                    orderStatus = " "
                    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text = call.message.text + f'\nЗаказ отменен. Сообщение для пользователя: Заказ отменен. Мы свяжемся с вами лично для уточнения деталей.',
                        reply_markup=None)
                    okOrderId = call.data.partition("cancel")[2]
                    orderStatus = db.get_orderStatus(okOrderId)
                    db.set_orderStatus(okOrderId, "Canceled") 
                    orderStatus = db.get_orderStatus(okOrderId)
                    user_id = db.get_user_id_through_order_id(okOrderId)
                    await bot.send_message(user_id, "Заказ отменен. Мы свяжемся с Вами лично для уточнения деталей.")

                elif "Оплатить" == call.message.reply_markup.inline_keyboard[0][0].text:
                    print ("Оплата")
                    paymentOrderId = call.message.reply_markup.inline_keyboard[0][0].callback_data
                         # remove inline buttons
                    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text = call.message.text,
                        reply_markup=nav.paymentOptionsMarkup())
                    user_id = call.message.chat.id
                    db.set_update(paymentOrderId)
                    order_inform = "Заказ находится на стадии оплаты \n" + "Пользователь: " + db.get_nickname(user_id) + db.get_order_through_order_id(paymentOrderId) 
                    msg = await bot.send_message(adminId, order_inform, reply_markup = nav.paymentComplitedMarkup(paymentOrderId))
                    db.set_message_id(paymentOrderId, msg["message_id"])

                elif "Оплата за заказ получена" == call.message.reply_markup.inline_keyboard[0][0].text:
                    print("Оплата за заказ получена")
                    paymentOrderId = call.message.reply_markup.inline_keyboard[0][0].callback_data
                    db.set_orderStatus(paymentOrderId, "complitedPayment") 
                    user_id = db.get_user_id_through_order_id(paymentOrderId)
                    order_inform = "Оплата за заказ получена \n" + "Пользователь: " + db.get_nickname(user_id) + db.get_paid_order_through_order_id(paymentOrderId) 
                    order_inform_for_user = "Оплата за заказ получена \n" + db.get_paid_order_through_order_id(paymentOrderId) 
                                    # remove inline buttons
                    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text = order_inform,
                        reply_markup=nav.orderRedeemedMurkup(paymentOrderId))
                    await bot.send_message(user_id, order_inform_for_user)

                elif "Заказ выкуплен" == call.message.reply_markup.inline_keyboard[0][0].text:
                    print("orderRedeemed")
                    redeemedOrderId = call.message.reply_markup.inline_keyboard[0][0].callback_data
                    db.set_orderStatus(redeemedOrderId, "orderRedeemed") 
                    user_id = db.get_user_id_through_order_id(redeemedOrderId)
                    order_inform = "Заказ выкуплен \n" + "Пользователь: " + db.get_nickname(user_id) + db.get_paid_order_through_order_id(redeemedOrderId) 
                    order_inform_for_user = "Заказ выкуплен \n" + db.get_paid_order_through_order_id(redeemedOrderId) + "Ожидайте уведомления о стоимости доставки\n" 
                    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text = order_inform + "\nВведите сумму доставки в евро:",
                        reply_markup=None)
                    db.set_orderStatus(redeemedOrderId, "orderRedeemed")
                    await bot.send_message(user_id, order_inform_for_user)

                elif "Оплатить доставку" == call.message.reply_markup.inline_keyboard[0][0].text:
                    print ("Оплата доставки")
                    deliveryPaymentOrderId = call.message.reply_markup.inline_keyboard[0][0].callback_data
                    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text = call.message.text,
                        reply_markup=nav.paymentOptionsMarkup())
                    user_id = call.message.chat.id
                    order_inform = "Заказ на стадии оплаты доставки\n" + "Пользователь: " + db.get_nickname(user_id) + db.get_delivery_paid_order_through_order_id(deliveryPaymentOrderId) 
                    msg = await bot.send_message(adminId, order_inform, reply_markup = nav.deliveryPaymentComplitedMarkup(deliveryPaymentOrderId))
                    db.set_message_id(deliveryPaymentOrderId, msg['message_id'])
                elif "Оплата за доставку получена" == call.message.reply_markup.inline_keyboard[0][0].text:
                    print("Оплата за доставку получена")
                    deliveryPaymentOrderId = call.message.reply_markup.inline_keyboard[0][0].callback_data
                    db.set_orderStatus(deliveryPaymentOrderId, "paidOrderDelivery") 
                    user_id = db.get_user_id_through_order_id(deliveryPaymentOrderId)
                    order_inform = "Оплата за доставку получена \n" + "Пользователь: " + db.get_nickname(user_id) + db.get_delivery_paid_order_through_order_id(deliveryPaymentOrderId) 
                    order_inform_for_user = "Оплата за доставку получена \n" + db.get_delivery_paid_order_through_order_id(deliveryPaymentOrderId) 
                    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text = order_inform,
                        reply_markup=nav.sentOrderMurkup(deliveryPaymentOrderId))
                    await bot.send_message(user_id, order_inform_for_user)
                elif "Заказ отправлен" == call.message.reply_markup.inline_keyboard[0][0].text:
                    print("Заказ отправлен")
                    sentOrderId = call.message.reply_markup.inline_keyboard[0][0].callback_data
                    db.set_orderStatus(sentOrderId, "sentOrder") 
                    user_id = db.get_user_id_through_order_id(sentOrderId)
                    db.set_update(sentOrderId)
                    order_inform = "Заказ отправлен \n" + "Пользователь: " + db.get_nickname(user_id) + db.get_delivery_paid_order_through_order_id(sentOrderId) 
                    order_inform_for_user = "Заказ отправлен \n" + db.get_delivery_paid_order_through_order_id(sentOrderId)
                    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text = order_inform,
                        reply_markup=None)
                    await bot.send_message(user_id, order_inform_for_user)
                elif "change" in call.data:
                    print("Изменить заказы")
                    s = call.message.text
                    result = re.findall("📦Номер заказа - \d+", s)
                    mystr = ' '.join(map(str,result))
                    number_result = [int(number_result) for number_result in str.split(mystr) if number_result.isdigit()]
                    for item in number_result:
                        answer = db.get_order_through_order_id(item)
                        await bot.send_message(adminId, answer, reply_markup = nav.changesMarkup())
                elif "delete" in call.data:
                    orderId = orderIdFromMessege(call.message.text)
                    db.delete_order(orderId)
                    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text = "Заказ удален!",
                        reply_markup=None)
                elif "edit" in call.data:
                    print("Редактировние наименования заказа edit")
                    await bot.send_message(adminId, "Функция Редактирование - в разработке 🔧")
     
    except Exception as e:
        print(repr(e))
def fanc():
    executor.start_polling(dp, skip_updates=True)

if __name__ =="__main__":
    Process(target = fanc).start()
    Process(target = httpd.serve_forever).start() 