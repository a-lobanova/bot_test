import sqlite3
from const import Const
const = Const

class Database:
	def __init__(self, db_file):
		self.connection = sqlite3.connect(db_file)
		self.cursor = self.connection.cursor()

	def add_user(self, user_id):
		with self.connection:
			return self.cursor.execute("INSERT INTO 'users' ('user_id') VALUES (?)", (user_id,))

	def user_exists(self, user_id):
		with self.connection:
			result = self.cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,)).fetchall()
			return bool(len(result))

	def order_exists(self, order_id):
		with self.connection:
			result = self.cursor.execute("SELECT * FROM orders WHERE order_id = ?", (order_id,)).fetchall()
			return bool(len(result))

	def order_status_exists(self, status):
		with self.connection:
			result = self.cursor.execute("SELECT * FROM orders WHERE status = ?", (status,)).fetchall()
			return bool(len(result))


	def get_order_id(self, status):
			with self.connection:
				result = self.cursor.execute("SELECT order_id FROM orders WHERE status = ?", (status,))
				return result.fetchone()[0]

	def get_user_id_through_order_id(self, order_id):
			with self.connection:
				result = self.cursor.execute("SELECT user_id FROM orders WHERE order_id = ?", (order_id,)).fetchall()
				for row in result:
					user_id = row[0]
				return user_id


	def get_user_id(self, user_id):
		result = self.cursor.execute ("SELECT user_id FROM users WHERE user_id = ?", (user_id,))
		return result.fetchone()[0]

	def set_nickname(self, user_id, nickname):
		with self.connection:
			return self.cursor.execute("UPDATE users SET nickname = ? WHERE user_id = ?", (nickname, user_id,))

	def set_contact(self, user_id, contact):
		with self.connection:
			return self.cursor.execute("UPDATE users SET contact = ? WHERE user_id = ?", (contact, user_id,))

	def set_signup(self, user_id, signup):
		with self.connection:
			return self.cursor.execute("UPDATE users SET signup = ? WHERE user_id = ?", (signup, user_id,))

	def set_orderStatus(self, order_id, status):
		with self.connection:
			return self.cursor.execute("UPDATE orders SET status = ? WHERE order_id = ?", (status, order_id,))

	def set_message_id(self, order_id, message_id):
		with self.connection:
			return self.cursor.execute("UPDATE orders SET message_id = ? WHERE order_id = ?", (message_id, order_id,))

	def set_update(self, order_id):
		with self.connection:
			return self.cursor.execute("UPDATE orders SET 'upDate' = DATETIME('now','localtime') WHERE order_id = ?", (order_id,))

	def get_message_id(self, order_id):
		with self.connection:
			result = self.cursor.execute("SELECT message_id FROM orders WHERE order_id = ?", (order_id,)).fetchall()
			for row in result:
				status1 = str(row[0])
			return status1

	def get_orderStatus(self, order_id):
		with self.connection:
			result = self.cursor.execute("SELECT status FROM orders WHERE order_id = ?", (order_id,)).fetchall()
			for row in result:
				status1 = str(row[0])
			return status1

	def set_rubprice(self, order_id, value):
		with self.connection:
			return self.cursor.execute("UPDATE orders SET rubprice = ? WHERE order_id = ?", (value, order_id,))

	def get_rubprice(self, order_id):
		with self.connection:
			result = self.cursor.execute("SELECT rubprice FROM orders WHERE order_id = ?", (order_id,)).fetchall()
			for row in result:
				rubprice = row[0]
			return rubprice	


	def get_orderDesc(self, order_id):
		with self.connection:
			result = self.cursor.execute("SELECT orderDesc FROM orders WHERE order_id = ?", (order_id,)).fetchall()
			for row in result:
				orderDesc = str(row[0])
			return orderDesc	


	def set_deliveryrubprice(self, order_id, value):
		with self.connection:
			return self.cursor.execute("UPDATE orders SET rubDeliveryPrice = ? WHERE order_id = ?", (value, order_id,))

	def get_deliveryrubprice(self, order_id):
		with self.connection:
			result = self.cursor.execute("SELECT rubDeliveryPrice FROM orders WHERE order_id = ?", (order_id,)).fetchall()
			for row in result:
				rubprice = row[0]
			return rubprice
	
	def editOrder(self, order_id, text):
		# print("def editOrder")
		# print("def editOrder text", text)
		with self.connection:
			return self.cursor.execute("UPDATE orders SET orderDesc = ? WHERE order_id = ?", (text, order_id,))

	def get_signup(self, user_id):
		with self.connection:
			result = self.cursor.execute("SELECT signup FROM users WHERE user_id = ?", (user_id,)).fetchall()
			for row in result:
				signup = str(row[0])
			return signup

	def get_nickname(self, user_id):
		with self.connection:
			result = self.cursor.execute("SELECT nickname FROM users WHERE user_id = ?", (user_id,)).fetchall()
			for row in result:
				nickname = str(row[0])
			return nickname

	def get_contact(self, user_id):
		with self.connection:
			result = self.cursor.execute("SELECT contact FROM users WHERE user_id = ?", (user_id,)).fetchall()
			for row in result:
				contact = str(row[0])
			return contact

	def add_order(self, user_id, order):
		with self.connection:
			return self.cursor.execute("INSERT INTO orders ('user_id', 'orderDesc') VALUES (?,?)", (self.get_user_id(user_id), order,))
	
	def get_lastOrder(self, user_id):
		with self.connection:
			# print(f'get_orders, userId = {user_id}')
			result = self.cursor.execute("SELECT * FROM orders WHERE user_id = ? ORDER BY order_id DESC LIMIT 1", (user_id,)).fetchall()
			answ = f" \n"
			for r in result:
				answ += f"Номер заказа - {r[0]}\n"
				answ += f"Наименование - {r[2]}\n"
				answ += f"Дата ({r[3]})\n"
			return answ

	def get_order_through_order_id(self, order_id):
		with self.connection:
			# print(f'get_orders, userId = {user_id}')
			result = self.cursor.execute("SELECT * FROM orders WHERE order_id = ?", (order_id,)).fetchall()
			answ = f" \n"
			for r in result:
				answ += f"Номер заказа - {r[0]}\n"
				answ += f"Наименование - {r[2]}\n"
				answ += f"Дата ({r[3]})\n"
			return answ

	def get_orderDesc_through_order_id(self, order_id):
		with self.connection:
			# print(f'get_orders, userId = {user_id}')
			result = self.cursor.execute("SELECT orderDesc FROM orders WHERE order_id = ?", (order_id)).fetchone()[0]
			# answ = f" \n"
			# for r in result:
			# 	answ += f"Номер заказа - {r[0]}\n"
			# 	answ += f"Наименование - {r[2]}\n"
			# 	answ += f"Дата ({r[3]})\n"
			return result

	def get_paid_order_through_order_id(self, order_id):
		with self.connection:
			# print(f'get_orders, userId = {user_id}')
			result = self.cursor.execute("SELECT * FROM orders WHERE order_id = ?", (order_id,)).fetchall()
			answ = f" \n"
			for r in result:
				answ += f"Сумма заказа - {r[7]}руб.\n"
				answ += f"Номер заказа - {r[0]}\n"
				answ += f"Наименование - {r[2]}\n"
				answ += f"Дата обновления - {r[10]}\n"
			return answ
	def get_delivery_paid_order_through_order_id(self, order_id):
		with self.connection:
			# print(f'get_orders, userId = {user_id}')
			result = self.cursor.execute("SELECT * FROM orders WHERE order_id = ?", (order_id,)).fetchall()
			answ = f" \n"
			for r in result:
				answ += f"Сумма заказа - {r[7]}руб.\n"
				answ += f"Сумма доставки - {r[9]}руб.\n"
				answ += f"Номер заказа - {r[0]}\n"
				answ += f"Наименование - {r[2]}\n"
				answ += f"Дата обновления - {r[10]}\n"
			return answ

	def get_lastOrder_id(self, user_id):
			with self.connection:
				result = self.cursor.execute("SELECT * FROM orders WHERE user_id = ? ORDER BY order_id DESC LIMIT 1", (user_id,))
				return result.fetchone()[0]

	def get_orders(self, user_id):
		with self.connection:
			result = self.cursor.execute("SELECT * FROM orders WHERE user_id = ? ORDER BY 'date'", (user_id,)).fetchall()
			return result
	def get_all_orders(self):
		with self.connection:
			result = self.cursor.execute("SELECT * FROM orders ORDER BY 'date'").fetchall()
			return result
	def get_all_orders_in_time(self, within = "all"):
		with self.connection:
			if (within == const.day):
				result = self.cursor.execute("SELECT * FROM orders WHERE date BETWEEN datetime('now', 'start of day') AND datetime('now', 'localtime') ORDER BY 'date'").fetchall()
			elif (within == const.week):
				result = self.cursor.execute("SELECT * FROM orders WHERE date BETWEEN datetime('now', '-6 days') AND datetime('now', 'localtime') ORDER BY date").fetchall()
			elif (within == const.2weeks):
				result = self.cursor.execute("SELECT * FROM orders WHERE date BETWEEN datetime('now', '-13 days') AND datetime('now', 'localtime') ORDER BY date").fetchall()
			elif (within == const.month):
				result = self.cursor.execute("SELECT * FROM orders WHERE date BETWEEN datetime('now', 'start of month') AND datetime('now', 'localtime') ORDER BY date").fetchall()
			else:	
				result = self.cursor.execute("SELECT * FROM orders ORDER BY 'date'").fetchall()
			return result

	def set_price(self, order_id, price):
		with self.connection:
			return self.cursor.execute("UPDATE orders SET price = ? WHERE order_id = ?", (price, order_id,))
	
	def set_delivery_price(self, order_id, deliveryPrice):
		with self.connection:
			return self.cursor.execute("UPDATE orders SET deliveryPrice = ? WHERE order_id = ?", (deliveryPrice, order_id,))			
	
	def get_users_status(self):
		with self.connection:
			result = self.cursor.execute("SELECT * FROM users").fetchall()
			return result

	def delete_order(self, order_id):
		with self.connection:
			return self.cursor.execute("DELETE FROM orders WHERE order_id = ?", (order_id))
		self.connection.commit()

	def close(self):
        # Закрываем соединение с БД
		self.connection.close()