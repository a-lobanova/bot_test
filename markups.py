from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

from const import Const
const = Const

btnProfile = KeyboardButton (const.myOrders)
btnOrder = KeyboardButton (const.createOrder)
bthAllOrders = KeyboardButton (const.allOrders)

btnGetContact = KeyboardButton('Отправить свой номер', request_contact = True)


def createMarkup(data):
	markup = InlineKeyboardMarkup(row_width=2)
	item1 = InlineKeyboardButton("Подтвердить заказ", callback_data = "ok" + str(data))
	item2 = InlineKeyboardButton("Отменить заказ", callback_data = "cancel" + str(data))
	markup.add(item1, item2)
	return markup

def paymentMarkup(data):
	payment = InlineKeyboardMarkup(row_width=1)
	item1 = InlineKeyboardButton("Оплатить", callback_data = data)
	payment.add(item1)
	return payment

def paymentOptionsMarkup():
	paymentOptions = InlineKeyboardMarkup(row_width=2)
	item1 = InlineKeyboardButton("По реквизитам", callback_data = "bankDetails")
	item2 = InlineKeyboardButton("Через ЮКассу", callback_data = "UKassa")
	paymentOptions.add(item1, item2)
	return paymentOptions

def paymentComplitedMarkup(data):
	paymentComplited = InlineKeyboardMarkup(row_width=1)
	item1 = InlineKeyboardButton("Оплата за заказ получена", callback_data=data)
	paymentComplited.add(item1)
	return paymentComplited

def orderRedeemedMurkup(data):
	orderRedeemed = InlineKeyboardMarkup(row_width=1)
	item1 = InlineKeyboardButton("Заказ выкуплен", callback_data=data)
	orderRedeemed.add(item1)
	return orderRedeemed

def deliveryPaymentMarkup(data):
	deliveryPayment = InlineKeyboardMarkup(row_width=1)
	item1 = InlineKeyboardButton("Оплатить доставку", callback_data=data)
	deliveryPayment.add(item1)
	return deliveryPayment

def deliveryPaymentComplitedMarkup(data):
	deliveryPaymentComplited = InlineKeyboardMarkup(row_width=1)
	item1 = InlineKeyboardButton("Оплата за доставку получена", callback_data=data)
	deliveryPaymentComplited.add(item1)
	return deliveryPaymentComplited

def sentOrderMurkup(data):
	sentOrder = InlineKeyboardMarkup(row_width=1)
	item1 = InlineKeyboardButton("Заказ отправлен", callback_data=data)
	sentOrder.add(item1)
	return sentOrder

def allOrdersMarkup():
	allOrders = ReplyKeyboardMarkup(resize_keyboard = True)
	item1 = KeyboardButton (const.day)
	item2 = KeyboardButton (const.week)
	item3 = KeyboardButton (const.twoWeeks)
	item4 = KeyboardButton (const.month)
	item5 = KeyboardButton (const.allTime)
	item6 = KeyboardButton ('❌ Отмена')
	allOrders.add(item1, item2, item3, item4, item5, item6)
	return allOrders

def changeMarkup():
	change = InlineKeyboardMarkup(row_width=1)
	item1 = InlineKeyboardButton("Изменить", callback_data= "change")
	change.add(item1)
	return change

def changesMarkup():
	changes = InlineKeyboardMarkup(row_width=1)
	item1 = InlineKeyboardButton("✏️ Редактировать", callback_data= "edit")
	item2 = InlineKeyboardButton("❌ Удалить заказ", callback_data= "delete")
	# item3 = InlineKeyboardButton("⬅️ Назад", callback_data= "goback")
	changes.add(item1,item2)
	return changes

mainMenu = ReplyKeyboardMarkup(resize_keyboard = True)
getContac = ReplyKeyboardMarkup(resize_keyboard = True)
mainMenuAdmin = ReplyKeyboardMarkup(resize_keyboard = True)

mainMenu.add(btnProfile, btnOrder)
getContac.add(btnGetContact)
mainMenuAdmin.add(bthAllOrders)




