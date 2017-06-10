#!/usr/bin/env python
# coding=utf-8

import pymysql
'''
对数据库的增、删、改操作都要commit才能改变数据库中的内容，别忘了！！！
'''
#在ticket表中删除订单
def delete_ticket(pass_id, flight_id):
	sql = "DELETE from ticket WHERE pass_id = %s and flight_id = %s"
	para = []
	para.append(pass_id)
	para.append(flight_id)

	conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='961105', db='test1', use_unicode=True, charset="utf8")
	cursor = conn.cursor()
	rowsAffected = cursor.execute(sql, para)
	conn.commit()
	cursor.close()

	if rowsAffected > 0:
		return True
	else:
		return False

#在flight中查询票价
def query_flight(flight_id, aclass):
	sql = "SELECT "
	if aclass == '经济舱':
		sql += "tourist_price "
	else:
		sql += "first_price "
	sql += "from flight WHERE id = %s"

	conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='961105', db='test1', use_unicode=True, charset="utf8")
	cursor = conn.cursor()
	cursor.execute(sql, (flight_id))
	row = cursor.fetchone()
	cursor.close()

	return row
	

#在ticket表中更新信息
def update_ticket(pass_id, flight_id, operation = 'pay'):
	if operation == 'pay':
		sql = "UPDATE ticket SET paid = %s WHERE pass_id = %s and flight_id = %s"
	true = True
	para = []
	para.append(true)
	para.append(pass_id)
	para.append(flight_id)

	conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='961105', db='test1', use_unicode=True, charset="utf8")
	cursor = conn.cursor()
	rowsAffected = cursor.execute(sql, para)
	conn.commit()
	cursor.close()

	if rowsAffected > 0:
		return True
	else:
		return False

#在passenger表中插入信息
def insert_passenger(pass_id, name, cellnumber):
	sql = "INSERT INTO passenger values(%s, %s, %s)"
	para = []
	para.append(pass_id)
	para.append(name)
	para.append(cellnumber)

	conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='961105', db='test1', use_unicode=True, charset="utf8")
	cursor = conn.cursor()
	rowsAffected = cursor.execute(sql, para)
	conn.commit()
	cursor.close()

	if rowsAffected > 0:
		return True
	else:
		return False

#在passenger表中查询旅客信息是否存在
def query_passenger(pass_id):
	sql = "SELECT * FROM passenger WHERE id = %s"

	conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='961105', db='test1', use_unicode=True, charset="utf8")
	cursor = conn.cursor()
	cursor.execute(sql, (pass_id))
	row = cursor.fetchone()
	cursor.close()

	if row:
		return True
	else:
		return False

#在ticket表中插入订单
def insert_ticket(pass_id, flight_id, aclass, price, printed = False, paid = False):
	sql = "INSERT INTO ticket values(%s, %s, %s, %s, %s, %s)"
	conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='961105', db='test1', use_unicode=True, charset="utf8")
	cursor = conn.cursor()
	rowsAffected = cursor.execute(sql, 
		(pass_id, flight_id, aclass, price, printed, paid))
	conn.commit()
	cursor.close()

	if rowsAffected > 0:
		return True
	else:
		return False

#在flight表中更新座位信息
def update_flight(flight_id, aclass, operation = 'add'):
	if aclass == 'tourist' or aclass == '经济舱':
		if operation == 'add':
			sql = "UPDATE flight SET tourist_reserved = tourist_reserved + 1"
		else:
			sql = "UPDATE flight SET tourist_reserved = tourist_reserved - 1"
	else:
		if operation == 'add':
			sql = "UPDATE flight SET first_reserved = first_reserved + 1"
		else:
			sql = "UPDATE flight SET first_reserved = first_reserved - 1"

	conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='961105', db='test1', use_unicode=True, charset="utf8")
	cursor = conn.cursor()
	rowsAffected = cursor.execute(sql)
	conn.commit()
	cursor.close()

	if rowsAffected > 0:
		return True
	else:
		return False

