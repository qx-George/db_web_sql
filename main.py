#!/usr/bin/env python
# coding=utf-8

import pymysql, sys
from sql import delete_ticket, insert_passenger, insert_ticket, update_flight, update_ticket, query_flight, query_passenger
from bottle import get, route, run, debug, template, request, static_file, error, redirect

reload(sys)
sys.setdefaultencoding('utf8')

@route('/main')
def main():
	return template('main')

#show signin page
@route('/signin')
def signin():
	error = ' '
	return template('signin', error = error)

#signin
@route('/signin', method = 'POST')
def do_signin():
	account = request.forms.get('account')
	password = request.forms.get('password')
	administrator = request.forms.get('administrator')
	error = '用户名或者密码错误！'
	if check_signin(administrator, account, password):
		if administrator == 'Administrator':
			return template('administrator')
		else:
			return template('passenger', rows = '', message = ' ')
	else: #密码验证错误，弹出相应的错误信息
		return template('signin', error = error)

#检查账号密码是否正确
def check_signin(administrator, account, password):
	#administrator
	if administrator == 'Administrator':
		if account == 'admin' and password == 'passwd':
			return True
		else:
			return False
	else:
		if account == 'pass' and password == 'passwd':
			return True
		else:
			return False

#info query module for passenger
@route('/passenger')
def passenger():
	if request.GET.save:
		depature_city = request.GET.depature_city.strip()
		arrival_city = request.GET.arrival_city.strip()
		time = request.GET.time.strip()
		aclass = request.GET.aclass.strip()

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
		result = cursor.fetchall()
		cursor.close()
		output = template('passenger', rows=result, aclass = aclass, message = ' ')
		return output
	#query all flight info by default
	else:
		conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='961105', db='test1', use_unicode=True, charset="utf8")
		cursor = conn.cursor()
		cursor.execute("SELECT company, id, departure_time, arrival_time, departure_airport, arrival_airport, tourist_price from flight")
		result = cursor.fetchall()
		cursor.close()
		output = template('passenger', rows=result, aclass = '经济舱', message = ' ') #默认传过去的是预订经济舱
		return output

#旅客预定机票页面，要通过查询界面传入航班号和舱位这2个参数
@route('/reserve/<flight_id>/<aclass>')
def reserve(flight_id, aclass):
	if check_seats(flight_id, aclass):
		return template('reserve', flight_id = flight_id, aclass = aclass)
	else:
		error = '对应舱位已经订满，预订失败！'
		return template('passenger', message = error)

#用户提交个人信息，完成预定
#1.session
#2.redirect
#3.绝对路径
@route('/reserve/<flight_id>/<aclass>', method = 'POST')
def do_reserve(flight_id, aclass):
	name = request.forms.get('name')
	pass_id = request.forms.get('pass_id')
	cellnumber = request.forms.get('cellnumber')

	#根据flight_id和aclass查询票价
	price = query_flight(flight_id, aclass)[0]
	#在插入乘客信息之前需要先查询其信息是否已经存在，不存在才插入
	if not query_passenger(pass_id):
		insert_passenger(pass_id, name, cellnumber)
	result1 = insert_ticket(pass_id, flight_id, aclass, price)
	#最后在flight表中更新座位信息
	result2 = update_flight(flight_id, aclass)

	if result1 and result2:
		message = '机票预定成功！'
	else:
		message = '机票预定失败！'

	return template('passenger', message = message, rows = '')

#退订机票
@route('/unsubscribe/<pass_id>/<flight_id>/<aclass>')
def unsubscribe(pass_id, flight_id, aclass):
	#首先在ticket表中删除订单
	ret1 = delete_ticket(pass_id, flight_id)
	#然后在flight表中更新座位信息
	ret2 = update_flight(flight_id, aclass, 'sub')
	if ret1 and ret2:
		message = '机票退订成功！'
	else:
		message = '机票退订失败！'

	return template('order', rows = show_order(), message = message)

@route('/pay/<pass_id>/<flight_id>')
def pay(pass_id, flight_id):
	ret = update_ticket(pass_id, flight_id)
	if ret:
		message = '机票付款成功！'
	else:
		message = '机票付款失败！'

	return template('order', rows = show_order(), message = message)


#检查座位是否已经订满
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

#查看订单
@route('/order')
def order():

	return template('order', rows = show_order(), message = ' ')

def show_order():
	sql = "SELECT pname, pass_id, cellnumber, flight_id, class, price, printed, paid from passenger, ticket where pass_id = passenger.id"
	conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='961105', db='test1', use_unicode=True, charset="utf8")
	cursor = conn.cursor()
	cursor.execute(sql)
	result = cursor.fetchall()
	cursor.close()

	return result

#查看航班信息
@route('/order/view/<flight_id>/<pclass>')
def order(flight_id, pclass):
	result  = view_flight(flight_id, pclass)
	if result:
		message = "航空公司  %s\\n航班号  %s\\n出发时间  %s\\n达到时间  %s\\n始发机场  %s\\n达到机场  %s\\n价格  %s\\n" % result
		return template('order', rows = show_order(), message = message)
	else:
		message = "未找到航班信息！"
		return template('order', rows = show_order(), message = message)

#查看航班信息
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

#info modify module
@route('/modify')
def modify():
	return template('modify')

#info delete module
@route('/delete', method='GET')
def delete():
	if request.GET.save:
		title = request.GET.title.strip()
		
		conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='961105', db='test1', use_unicode=True, charset="utf8")
		cursor = conn.cursor()
		cursor.execute("DELETE from book WHERE title = %s ", title)
		new_id = cursor.lastrowid

		conn.commit()
		cursor.close()

		return template('modify')
	else:
		return template('modify')

#info insert module
@route('/insert', method='GET')
def insert():
	if request.GET.save:
		title = request.GET.title.strip()
		writer = request.GET.writer.strip()
		pyear = request.GET.pyear.strip()
		pinstitution = request.GET.pinstitution.strip()
		plocation = request.GET.plocation.strip()
		page = request.GET.page.strip()
		
		conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='961105', db='test1', use_unicode=True, charset="utf8")
		cursor = conn.cursor()
		cursor.execute("INSERT INTO book values(%s, %s, %s, %s, %s, %s)", 
			(title, writer, pyear, pinstitution, plocation, page))
		new_id = cursor.lastrowid

		conn.commit()
		cursor.close()

		return template('modify')
	else:
		return template('modify')

#info update module
@route('/update', method='GET')
def update():
	if request.GET.save:
		old_title = request.GET.old_title.strip()
		title = request.GET.title.strip()
		writer = request.GET.writer.strip()
		pyear = request.GET.pyear.strip()
		pinstitution = request.GET.pinstitution.strip()
		plocation = request.GET.plocation.strip()
		page = request.GET.page.strip()
		
		count = 0	
		para = []
		sql = "UPDATE book SET"

		if title != '':
			sql += " title = %s"
			para.append(title)
			count += 1
		if writer != '':
			if count:
				sql += ","
			sql += " writer = %s"
			para.append(writer)
			count += 1
		if pyear:
			if count:
				sql += ","
			sql += " pyear = %s"
			para.append(pyear)
			count += 1
		if pinstitution != '':
			if count:
				sql += ","
			sql += " pinstitution = %s"
			para.append(pinstitution)
			count += 1
		if plocation != '':
			if count:
				sql += ","
			sql += " plocation = %s"
			para.append(plocation)
			count += 1
		if page:
			if count:
				sql += ","
			sql += " page = %s"
			para.append(page)
			count += 1

		if old_title != '':
			sql += " WHERE title LIKE " + "'" + old_title + "'"

			conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='961105', db='test1', use_unicode=True, charset="utf8")
			cursor = conn.cursor()
			cursor.execute(sql, tuple(para))
			new_id = cursor.lastrowid
			conn.commit()
			cursor.close()

		return template('modify')
	else:
		return template('modify')

@route('/show_all')
def show_all():
	return template('show_all')

@route('/jpg/<filename>')
def server_static(filename):
	return static_file(filename, root='./jpg/')

@route('/bootstrap-3.3.7-dist/css/<filename>')
def server_static(filename):
	return static_file(filename, root='./bootstrap-3.3.7-dist/css/')

@route('/bootstrap-3.3.7-dist/fonts/<filename>')
def server_static(filename):
	return static_file(filename, root='./bootstrap-3.3.7-dist/fonts/')

@route('/bootstrap-3.3.7-dist/js/<filename>')
def server_static(filename):
	return static_file(filename, root='./bootstrap-3.3.7-dist/js/')

debug(True)
run(reloader = True)