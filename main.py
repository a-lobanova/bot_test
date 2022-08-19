import logging
import telebot
import re
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types.message import ContentTypes
import markups as nav
from db import Database
from const import Const
# from yookassa import Payment
import requests
# from telebot import types

const = Const

# data = requests.get('https://www.cbr-xml-daily.ru/daily_json.js').json()
# https://www.tinkoff.ru/api/v1/currency_rates/
data = requests.get('https://www.tinkoff.ru/api/v1/currency_rates/').json()
rate = (data['payload']['rates'][72]['sell'])
print(rate)

TOKEN = const.token

logging.basicConfig(level = logging.INFO)

bot = Bot(token = TOKEN)

dp = Dispatcher(bot)

db = Database('database.db')

adminId = 416370888

# previosOrderStatus = "test"

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
    # print("call.message.text", text)
    s = text
    result = re.findall("Номер заказа - \d+", s)
    # print("result", result)
    # print("type result", type(result))
    mystr = ' '.join(map(str,result))
    # print("mystr", mystr)
    number_result = [int(number_result) for number_result in str.split(mystr) if number_result.isdigit()]
    # print("number_result", number_result)
    return(number_result)               

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
                        answer += f" - {r[2]}"
                        answer += f" ({r[3]})\n"
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
            # print("order_Id", order_id)
            # print("user_id", user_id)
            print("price", message.text)
            try:
                a = int(message.text)
                print("try", message.text)
                db.set_price(order_id, message.text)
                db.set_orderStatus(order_id, "wait payment")
                summa = round((int(message.text) + 50) * rate)
                await bot.send_message(user_id, "Заказ подтвержден." + "\nНомер заказа - " + str(order_id) +"\n Сумма к оплате, включая комисиию(50EUR): " + str(summa) + " руб. По курсу Тинькофф 1EUR = " + str(rate), reply_markup = nav.paymentMarkup(order_id))
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
        # elif(db.order_status_exists("edit")):
        #     print(" admin messege Редактирование заказа")
        #     order_id = db.get_order_id("edit")
        #     db.editOrder(order_id, message.text)
        #     db.set_orderStatus(previosOrderStatus)
        #     previosOrderStatus = 0

        elif message.text == 'Все заказы':
                await bot.send_message(adminId, "Выберите интервал времени", reply_markup = nav.allOrdersMarkup())
        elif message.text == "День":
                records = db.get_all_orders_in_time("day")
                if(records):
                    answer = dataOutput(records, message.text)
                    await bot.send_message(adminId, answer, reply_markup = nav.changeMarkup())
                else:
                    await message.reply("Записей не обнаружено!")
        elif message.text == "Неделя":
                records = db.get_all_orders_in_time("week")
                if(records):
                    answer = dataOutput(records, message.text)
                    await bot.send_message(adminId, answer, reply_markup = nav.changeMarkup())
                else:
                    await message.reply("Записей не обнаружено!")
        elif message.text == "Две недели":
                records = db.get_all_orders_in_time("2weeks")
                if(records):
                    answer = dataOutput(records, message.text)
                    await bot.send_message(adminId, answer, reply_markup = nav.changeMarkup())
                else:
                    await message.reply("Записей не обнаружено!")
        elif message.text == "Месяц":
                records = db.get_all_orders_in_time("month")
                if(records):
                    answer = dataOutput(records, message.text)
                    await bot.send_message(adminId, answer, reply_markup = nav.changeMarkup())
                else:
                    await message.reply("Записей не обнаружено!")
        elif message.text == "Все время":
                records = db.get_all_orders_in_time("all")
                if(records):
                    answer = dataOutput(records, message.text)
                    await bot.send_message(adminId, answer, reply_markup = nav.changeMarkup())
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
        await bot.send_message(userId, "Ошибка🤷‍♀️")

@dp.callback_query_handler(text = "bankDetails")
async def callback_inline(call: types.CallbackQuery):
    await bot.send_message(call.message.chat.id, const.bank_details)
    await bot.send_photo(call.message.chat.id, photo=open('static/qr.jpg', 'rb'))

@dp.callback_query_handler(text = "UKassa")
async def callback_inline(call: types.CallbackQuery):
    # print(" UKassa call", call)
    # order_id = orderIdFromMessege(call.message.text)
    orderId = str(orderIdFromMessege(call.message.text))
    f = filter(str.isdecimal, orderId)
    order_id = "".join(f)
    print ("order_id", order_id)
    if db.get_orderStatus(order_id) == "wait payment":
        print("db.get_orderStatus(order_id) == wait payment")
        amount = str(round(db.get_rubprice(order_id)))+"00"
        amountPrice = int(amount)
        description = db.get_orderDesc(order_id)
        print("orderDesc", description)
        await bot.send_invoice(chat_id = call.from_user.id, title = "Оплата заказа #" + order_id, description = description, payload = order_id, provider_token = const.UKassaTestToken,
            currency = "RUB", start_parameter = "test_bot", prices=[{"label":"Руб", "amount": amountPrice}])
        db.set_orderStatus(order_id, "yookassaPayment")
    elif db.get_orderStatus(order_id) == "wait delivery payment":
        print("db.get_orderStatus(order_id) == wait delivery payment")
        amount = str(round(db.get_deliveryrubprice(order_id)))+"00"
        amountPrice = int(amount)
        description = db.get_orderDesc(order_id)
        # print("orderDesc", description)
        await bot.send_invoice(chat_id = call.from_user.id, title = "Оплата ДОСТАВКИ заказа #" + order_id, description = description, payload = order_id, provider_token = const.UKassaTestToken,
            currency = "RUB", start_parameter = "test_bot", prices=[{"label":"Руб", "amount": amountPrice}])
        

@dp.pre_checkout_query_handler()
async def process_pre_chechout_query(pre_checkout_query: types.PreCheckoutQuery):
    print("process_pre_chechout_query", pre_checkout_query)
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok = True)
    # payment = Payment.cancellation_details.reason
    # print(payment)


@dp.message_handler(content_types=ContentTypes.SUCCESSFUL_PAYMENT)
async def process_pay(message: types.Message):
    # print("message", message)
    # print(ContentTypes.SUCCESSFUL_PAYMENT)
    # print("cancellation_details", Payment.cancellation_details)
    order_id = message.successful_payment.invoice_payload
    print("order_id", order_id)
    if db.order_exists(message.successful_payment.invoice_payload):
        # Уведомление об успешном платеже
        db.set_orderStatus(order_id, "complitedPayment")
        db.set_update(order_id) 
        user_id = db.get_user_id_through_order_id(order_id)
        order_inform = "Заказ оплачен через ЮКасса!\n" + "Пользователь: " + db.get_nickname(user_id) + db.get_paid_order_through_order_id(order_id) 
        # order_inform_for_user = "Оплата за заказ получена \n" + db.get_paid_order_through_order_id(order_id) 
        # remove inline buttons
        print("db.get_message_id(order_id)", db.get_message_id(order_id))
        await bot.edit_message_text(chat_id=adminId, message_id=db.get_message_id(order_id), text = order_inform)
        await bot.send_message(message.from_user.id, "Платеж принят!")
        await bot.send_message(adminId, order_inform, reply_markup=nav.orderRedeemedMurkup(order_id))

@dp.callback_query_handler()
async def callback_inline(call):
    print ("callback_query_handler")
    # print(call)
    # print("call.message.from_id",call.message.from_id)
    # print("call.message.chat.id",call.message.chat.id)
    try:
        if call.message:
            if call.data:
                print("call", call)
                # print("call.data", call.data)
                if "ok" in call.data:
                    print ("Подтвердить")
                    # print("call.message", call.message)
                    # print("test", call.message.reply_markup.inline_keyboard[0][0].callback_data)
                    okOrderId = call.data.partition("ok")[2]
                    db.set_update(okOrderId)
                    print("type(okOrderId)", type(okOrderId))
                        # remove inline buttons
                    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text = call.message.text + f'\nЗаказ подтвержден, введите сумму в евро к оплате. Курс на сегодня 1EUR = {rate} руб.',
                        reply_markup=None)
                    # await bot.send_message(call.message.chat.id, f'Заказ {okOrderId} подтвержден, введите сумму в евро к оплате. Курс на сегодня 1EUR = {rate} руб.')
                    db.set_orderStatus(okOrderId, "wait price") 
                elif "cancel" in call.data:
                    print ("Отменить заказ")
                    orderStatus = " "
                    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text = call.message.text + f'\nЗаказ отменен. Сообщение для пользователя: Заказ отменен. Мы свяжемся с вами лично для уточнения деталей.',
                        reply_markup=None)
                    # await bot.send_message(call.message.chat.id, 'Заказ отменен. Сообщение для пользователя: Заказ отменен. Мы свяжемся с вами лично для уточнения деталей.')
                    okOrderId = call.data.partition("cancel")[2]
                    print("okOrderId", okOrderId)
                    print("type(orderStatus)", type(okOrderId))
                    orderStatus = db.get_orderStatus(okOrderId)
                    print("type(orderStatus)", type(orderStatus))
                    print("1 orderStatus", orderStatus)
                    db.set_orderStatus(okOrderId, "Canceled") 
                    orderStatus = db.get_orderStatus(okOrderId)
                    print(" 2 orderStatus", orderStatus)
                    user_id = db.get_user_id_through_order_id(okOrderId)
                    await bot.send_message(user_id, "Заказ отменен. Мы свяжемся с Вами лично для уточнения деталей.")
                elif "Оплатить" == call.message.reply_markup.inline_keyboard[0][0].text:
                    print ("Оплата")
                    print("Оплата call",call)
                    paymentOrderId = call.message.reply_markup.inline_keyboard[0][0].callback_data
                    # print("paymentOrderId", paymentOrderId)
                         # remove inline buttons
                    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text = call.message.text,
                        reply_markup=nav.paymentOptionsMarkup())
                    user_id = call.message.chat.id
                    db.set_update(paymentOrderId)
                    order_inform = "Заказ находится на стадии оплаты \n" + "Пользователь: " + db.get_nickname(user_id) + db.get_order_through_order_id(paymentOrderId) 
                    msg = await bot.send_message(adminId, order_inform, reply_markup = nav.paymentComplitedMarkup(paymentOrderId))
                    # print(msg["message_id"])
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
                    # await bot.send_message(adminId, order_inform, reply_markup=nav.orderRedeemedMurkup(paymentOrderId))
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
                    # await bot.send_message(adminId, order_inform)
                    db.set_orderStatus(redeemedOrderId, "orderRedeemed")
                    # await bot.send_message(adminId, "Введите сумму доставки:")
                    await bot.send_message(user_id, order_inform_for_user)
                elif "Оплатить доставку" == call.message.reply_markup.inline_keyboard[0][0].text:
                    print ("Оплата доставки")
                    print("call.message.from_id",call.message.from_id)
                    deliveryPaymentOrderId = call.message.reply_markup.inline_keyboard[0][0].callback_data
                    print("call.message.chat.id",call.message.chat.id)
                    print("deliveryPaymentOrderId", deliveryPaymentOrderId)
                    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text = call.message.text,
                        reply_markup=nav.paymentOptionsMarkup())
                    # await bot.send_message(call.message.chat.id, const.bank_details)
                    # await bot.send_photo(call.message.chat.id, photo=open('static/qr.jpg', 'rb'))
                    user_id = call.message.chat.id
                    order_inform = "Заказ на стадии оплаты доставки\n" + "Пользователь: " + db.get_nickname(user_id) + db.get_delivery_paid_order_through_order_id(deliveryPaymentOrderId) 
                    await bot.send_message(adminId, order_inform, reply_markup = nav.deliveryPaymentComplitedMarkup(deliveryPaymentOrderId))
                elif "Оплата за доставку получена" == call.message.reply_markup.inline_keyboard[0][0].text:
                    print("Оплата за доставку получена")
                    deliveryPaymentOrderId = call.message.reply_markup.inline_keyboard[0][0].callback_data
                    db.set_orderStatus(deliveryPaymentOrderId, "paidOrderDelivery") 
                    user_id = db.get_user_id_through_order_id(deliveryPaymentOrderId)
                    order_inform = "Оплата за доставку получена \n" + "Пользователь: " + db.get_nickname(user_id) + db.get_delivery_paid_order_through_order_id(deliveryPaymentOrderId) 
                    order_inform_for_user = "Оплата за доставку получена \n" + db.get_delivery_paid_order_through_order_id(deliveryPaymentOrderId) 
                    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text = order_inform,
                        reply_markup=nav.sentOrderMurkup(deliveryPaymentOrderId))
                    # await bot.send_message(adminId, order_inform, reply_markup=nav.sentOrderMurkup(deliveryPaymentOrderId))
                    await bot.send_message(user_id, order_inform_for_user)
                elif "Заказ отправлен" == call.message.reply_markup.inline_keyboard[0][0].text:
                    print("Заказ отправлен")
                    sentOrderId = call.message.reply_markup.inline_keyboard[0][0].callback_data
                    db.set_orderStatus(sentOrderId, "sentOrder") 
                    user_id = db.get_user_id_through_order_id(sentOrderId)
                    order_inform = "Заказ отправлен \n" + "Пользователь: " + db.get_nickname(user_id) + db.get_delivery_paid_order_through_order_id(sentOrderId) 
                    order_inform_for_user = "Заказ отправлен \n" + db.get_delivery_paid_order_through_order_id(sentOrderId)
                    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text = order_inform,
                        reply_markup=None)
                    await bot.send_message(user_id, order_inform_for_user)
                elif "change" in call.data:
                    print("Изменить заказы")
                    print("call.message.text", call.message.text)
                    s = call.message.text
                    result = re.findall("📦Номер заказа - \d+", s)
                    print("result", result)
                    print("type result", type(result))
                    mystr = ' '.join(map(str,result))
                    print("mystr", mystr)
                    number_result = [int(number_result) for number_result in str.split(mystr) if number_result.isdigit()]
                    print("number_result", number_result)
                    print("number_result", type(number_result))
                    for item in number_result:
                        print("item", item)
                        print("item", type(item))
                        answer = db.get_order_through_order_id(item)
                        await bot.send_message(adminId, answer, reply_markup = nav.changesMarkup())
                elif "delete" in call.data:
                    orderId = orderIdFromMessege(call.message.text)
                    print("number_result", orderId)
                    db.delete_order(orderId)
                    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text = "Заказ удален!",
                        reply_markup=None)
                elif "edit" in call.data:
                    # global previosOrderStatus
                    print("Редактировние наименования заказа edit")
                    # orderId = str(orderIdFromMessege(call.message.text))
                    # f = filter(str.isdecimal, orderId)
                    # orderId1 = "".join(f)
                    # orderStatus = ""
                    # orderStatus = db.get_orderStatus(orderId1)
                    # db.set_orderStatus(orderId1, "orderEdit") 
                    # orderStatus = db.get_orderStatus(orderId1)
                    await bot.send_message(adminId, "Функция Редактирование - в разработке 🔧")






                
                
                    
                # if call.data == 'good':
                #     # await bot.send_message(call.message.chat.id, 'Заказ подтвержден, введите сумму к оплате: ')
                #     print("call.message.chat.id",call.message.chat.id)
                # elif call.data == 'bad':
                #     await bot.send_message(call.message.chat.id, 'Заказ отменен')
     
                # remove inline buttons
            # await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text = call.message.text,
            #     reply_markup=None)
     
                # # show alert
                # await bot.answer_callback_query(callback_query_id=call.id, show_alert=False,
                #     text="ЭТО ТЕСТОВОЕ УВЕДОМЛЕНИЕ!!11")
     
    except Exception as e:
        print(repr(e))

if __name__ =="__main__":
    executor.start_polling(dp,skip_updates = True)