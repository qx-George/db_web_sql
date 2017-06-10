#!/usr/bin/env python
# coding=utf-8

import pymysql
'''
对数据库的增、删、改操作都要commit才能改变数据库中的内容，别忘了！！！
'''
'''
flight 表的相关操作
'''
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

#在flight表中更新所有信息
def update_flight_all(old_flight_id, flight_id, company, plane_type, departure_airport, arrival_airport,
	departure_time, arrival_time, tourist_reserved, first_reserved, tourist_price, first_price):
	count = 0
	para = []
	sql = "UPDATE flight SET"

	if flight_id != '':
		sql += " id = %s"
		para.append(flight_id)
		count += 1
	if company != '':
		if count:
			sql += ","
		sql += " company = %s"
		para.append(company)
		count += 1
	if plane_type != '':
		if count:
			sql += ","
		sql += " plane_type = %s"
		para.append(plane_type)
		count += 1
	if departure_airport != '':
		if count:
			sql += ","
		sql += " departure_airport = %s"
		para.append(departure_airport)
		count += 1
	if arrival_airport != '':
		if count:
			sql += ","
		sql += " arrival_airport = %s"
		para.append(arrival_airport)
		count += 1
	if departure_time != '':
		if count:
			sql += ","
		sql += " departure_time = %s"
		para.append(departure_time)
		count += 1
	if arrival_time != '':
		if count:
			sql += ","
		sql += " arrival_time = %s"
		para.append(arrival_time)
		count += 1
	if tourist_reserved:
		if count:
			sql += ","
		sql += " tourist_reserved = %s"
		para.append(tourist_reserved)
		count += 1
	if first_reserved:
		if count:
			sql += ","
		sql += " first_reserved = %s"
		para.append(first_reserved)
		count += 1
	if tourist_price:
		if count:
			sql += ","
		sql += " tourist_price = %s"
		para.append(tourist_price)
		count += 1
	if first_price:
		if count:
			sql += ","
		sql += " first_price = %s"
		para.append(first_price)
		count += 1 
	sql += " WHERE id LIKE " + "'" + old_flight_id + "'"
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
#给flight_id和aclass给了默认参数，方便复用此函数
def query_flight(flight_id = -1, aclass = '经济舱'):
	if flight_id == -1:
		sql = "SELECT * FROM flight"
	else:
		sql = "SELECT "
		if aclass == '经济舱':
			sql += "tourist_price "
		else:
			sql += "first_price "
		sql += "from flight WHERE id = %s"

	conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='961105', db='test1', use_unicode=True, charset="utf8")
	cursor = conn.cursor()
	if flight_id == -1:
		cursor.execute(sql)
		row = cursor.fetchall()
	else:
		cursor.execute(sql, (flight_id))
		row = cursor.fetchone()
	cursor.close()

	return row

#查看特定航班信息，从旅客订单页面发出请求
def view_flight(flight_id, pclass):
	sql = "SELECT company, id, departure_time, arrival_time, departure_airport, arrival_airport, " 
	if pclass == '经济舱':
		sql += "tourist_price "
	else:
		sql += "first_price "
	sql += "from flight "
	sql += "WHERE id = %s"

	para = []
	para.append(flight_id)
	conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='961105', db='test1', use_unicode=True, charset="utf8")
	cursor = conn.cursor()
	cursor.execute(sql, para)
	result = cursor.fetchone()
	cursor.close()

	return result

#往flight表中插入信息
def insert_flight(flight_id, company, plane_type, departure_airport, arrival_airport,
	departure_time, arrival_time, tourist_reserved, first_reserved, tourist_price, first_price):
	
	sql = "INSERT INTO flight values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
	para = []
	para.append(flight_id)
	para.append(company)
	para.append(plane_type)
	para.append(departure_airport)
	para.append(arrival_airport)
	para.append(departure_time)
	para.append(arrival_time)
	para.append(tourist_reserved)
	para.append(first_reserved)
	para.append(tourist_price)
	para.append(first_price)

	conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='961105', db='test1', use_unicode=True, charset="utf8")
	cursor = conn.cursor()
	rowsAffected = cursor.execute(sql, para)
	conn.commit()
	cursor.close()

	if rowsAffected > 0:
		return True
	else:
		return False

#在flight表中删除元组
def delete_flight(flight_id):
	sql = "DELETE FROM flight WHERE id = %s"

	conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='961105', db='test1', use_unicode=True, charset="utf8")
	cursor = conn.cursor()
	rowsAffected = cursor.execute(sql, (flight_id))
	conn.commit()
	cursor.close()

	if rowsAffected > 0:
		return True
	else:
		return False


'''
airport 表的相关操作
'''
#在airport表中查询信息
def query_airport():
	sql = "SELECT * FROM airport"

	conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='961105', db='test1', use_unicode=True, charset="utf8")
	cursor = conn.cursor()
	cursor.execute(sql)
	rows = cursor.fetchall()
	cursor.close()

	return rows

#往airport表中插入信息
def insert_airport(airport, city):
	
	sql = "INSERT INTO airport values(%s, %s)"
	para = []
	para.append(airport)
	para.append(city)

	conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='961105', db='test1', use_unicode=True, charset="utf8")
	cursor = conn.cursor()
	rowsAffected = cursor.execute(sql, para)
	conn.commit()
	cursor.close()

	if rowsAffected > 0:
		return True
	else:
		return False

#在airport表中删除元组
def delete_airport(airport):
	sql = "DELETE FROM airport WHERE airport = %s"

	conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='961105', db='test1', use_unicode=True, charset="utf8")
	cursor = conn.cursor()
	rowsAffected = cursor.execute(sql, (airport))
	conn.commit()
	cursor.close()

	if rowsAffected > 0:
		return True
	else:
		return False

#在airport表中更新所有信息
def update_airport(old_airport, airport, city):
	count = 0
	para = []
	sql = "UPDATE airport SET"

	if airport != '':
		sql += " airport = %s"
		para.append(airport)
		count += 1
	if city != '':
		if count:
			sql += ","
		sql += " city = %s"
		para.append(city)
		count += 1

	sql += " WHERE airport LIKE " + "'" + old_airport + "'"
	conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='961105', db='test1', use_unicode=True, charset="utf8")
	cursor = conn.cursor()
	rowsAffected = cursor.execute(sql, para)
	conn.commit()
	cursor.close()

	if rowsAffected > 0:
		return True
	else:
		return False

'''
plane_type 表的相关操作
'''
#在plane_type表中查询信息
def query_plane_type():
	sql = "SELECT * FROM plane_type"

	conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='961105', db='test1', use_unicode=True, charset="utf8")
	cursor = conn.cursor()
	cursor.execute(sql)
	rows = cursor.fetchall()
	cursor.close()

	return rows

#往plane_type表中插入信息
def insert_plane_type(plane_type, tourist_class, first_class):
	
	sql = "INSERT INTO plane_type values(%s, %s, %s)"
	para = []
	para.append(plane_type)
	para.append(tourist_class)
	para.append(first_class)

	conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='961105', db='test1', use_unicode=True, charset="utf8")
	cursor = conn.cursor()
	rowsAffected = cursor.execute(sql, para)
	conn.commit()
	cursor.close()

	if rowsAffected > 0:
		return True
	else:
		return False

#在plane_type表中删除元组
def delete_plane_type(plane_type):
	sql = "DELETE FROM plane_type WHERE type = %s"

	conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='961105', db='test1', use_unicode=True, charset="utf8")
	cursor = conn.cursor()
	rowsAffected = cursor.execute(sql, (plane_type))
	conn.commit()
	cursor.close()

	if rowsAffected > 0:
		return True
	else:
		return False

#在plane_type表中更新所有信息
def update_plane_type(old_plane_type, plane_type, tourist_class, first_class):
	count = 0
	para = []
	sql = "UPDATE plane_type SET"

	if plane_type != '':
		sql += " type = %s"
		para.append(plane_type)
		count += 1
	if tourist_class != '':
		if count:
			sql += ","
		sql += " tourist_class = %s"
		para.append(tourist_class)
		count += 1
	if first_class != '':
		if count:
			sql += ","
		sql += " first_class = %s"
		para.append(first_class)
		count += 1

	sql += " WHERE type LIKE " + "'" + old_plane_type + "'"
	conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='961105', db='test1', use_unicode=True, charset="utf8")
	cursor = conn.cursor()
	rowsAffected = cursor.execute(sql, para)
	conn.commit()
	cursor.close()

	if rowsAffected > 0:
		return True
	else:
		return False


'''
passenger 表的相关操作
'''
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

'''
ticket 表的相关操作
'''
#在ticket表中查询对应的机票是否已经打印
def is_printed(pass_id, flight_id):
	sql = "SELECT printed FROM ticket WHERE pass_id = %s and flight_id = %s"
	para = []
	para.append(pass_id)
	para.append(flight_id)

	conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='961105', db='test1', use_unicode=True, charset="utf8")
	cursor = conn.cursor()
	cursor.execute(sql, para)
	row = cursor.fetchone()
	cursor.close()

	return row[0]

def query_ticket():
	sql = "SELECT * FROM ticket"

	conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='961105', db='test1', use_unicode=True, charset="utf8")
	cursor = conn.cursor()
	cursor.execute(sql)
	rows = cursor.fetchall()
	cursor.close()

	return rows

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

'''
对组合表的相关操作
'''
#通过对flight和airport表的组合查询完成旅客航班查询任务
def passenger_flight(depature_city, arrival_city, time, aclass):
	#首先由城市查到可能的机场
	para = []
	para.append(depature_city)
	para.append(arrival_city)
	para.append(time)
	sql = "SELECT company, id, departure_time, arrival_time, departure_airport, arrival_airport, "
	if aclass == '经济舱':
		sql += "tourist_price "
	else:
		sql += "first_price "
	sql += "from flight "
	sql += "WHERE departure_airport in "
	sql += "(SELECT airport from airport where city = %s) "
	sql += "and arrival_airport in "
	sql += "(SELECT airport from airport where city = %s) "
	sql += "and DATE_FORMAT(departure_time, '%%Y-%%m-%%d') = %s"
		
	conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='961105', db='test1', use_unicode=True, charset="utf8")
	cursor = conn.cursor()
	cursor.execute(sql, tuple(para))
	rows = cursor.fetchall()
	cursor.close()

	return rows

#在plane_type和flight表中检查座位是否已经订满
def check_seats(flight_id, aclass):
	conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='961105', db='test1', use_unicode=True, charset="utf8")
	cursor = conn.cursor()
	#首先由flight_id查出飞机的type
	para = []
	para.append(flight_id)
	sql = "SELECT plane_type, tourist_reserved, first_reserved from flight "
	sql += "WHERE id = %s"
	cursor.execute(sql, tuple(para))
	result = cursor.fetchone()

	flight_type = result[0]
	tourist_reserved = result[1]
	first_reserved = result[2]

	para = []
	para.append(flight_type)
	sql = "SELECT tourist_class, first_class from plane_type "
	sql += " WHERE type = %s"
	cursor.execute(sql, tuple(para))
	result = cursor.fetchone()
	cursor.close()

	tourist_class = result[0]
	first_class = result[1]

	if aclass == '经济舱':
		if tourist_reserved == tourist_class:
			return False
	else:
		if first_reserved == first_class:
			return False
	return True

#在passenger和ticket表中查询旅客订单信息
def show_order():
	sql = "SELECT pname, pass_id, cellnumber, flight_id, class, price, printed, paid from passenger, ticket where pass_id = passenger.id"
	conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='961105', db='test1', use_unicode=True, charset="utf8")
	cursor = conn.cursor()
	cursor.execute(sql)
	result = cursor.fetchall()
	cursor.close()

	return result