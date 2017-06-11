#!/usr/bin/env python
# coding=utf-8

from __future__ import division

import pymysql, sys
from bottle import get, route, run, debug, template, request, static_file, error, redirect
from sql import update_flight, query_flight, view_flight, insert_flight, delete_flight, update_flight_all, query_flight_seat
from sql import query_airport, insert_airport, delete_airport, update_airport
from sql import query_plane_type, insert_plane_type, delete_plane_type, update_plane_type
from sql import insert_passenger, query_passenger
from sql import is_printed, is_paid, query_ticket, update_ticket, insert_ticket, delete_ticket
#对表的组合操作
from sql import passenger_flight, check_seats, show_order

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
			return template('administrator', rows = '', message = ' ')
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

#旅客查询航班信息界面
@route('/passenger')
def passenger():
	depature_city = request.GET.depature_city.strip()
	arrival_city = request.GET.arrival_city.strip()
	time = request.GET.time.strip()
	aclass = request.GET.aclass.strip()

	if not aclass:
		aclass = '经济舱'
	result = passenger_flight(depature_city, arrival_city, time, aclass)
	
	return template('passenger', rows=result, aclass = '经济舱', message = ' ')


#管理员的主界面，默认显示所有的航班信息
@route('/administrator')
def administrator():
	result = query_flight()
	return template('administrator', rows = result, message = ' ')

#管理员的维护机场信息界面，默认显示所有的机场信息
@route('/airport')
def airport():
	result = query_airport()
	return template('airport', rows = result, message = ' ')

#管理员的维护机型信息界面，默认显示所有的机型信息
@route('/plane_type')
def plane_type():
	result = query_plane_type()
	return template('plane_type', rows = result, message = ' ')

#管理员的维护订单界面，默认显示所有的订单
@route('/maintain_order')
def maintain_order():
	result = query_ticket()
	return template('maintain_order', rows = result, message = ' ')


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
	#首先要检查机票是否已经打印，已经打印的机票不能退订
	if is_printed(pass_id, flight_id):
		message = '机票已经打印，无法退订！'
	else:
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


#旅客查看订单的页面
@route('/order')
def order():
	return template('order', rows = show_order(), message = ' ')

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

#航班信息添加操作
@route('/add_flight', method='GET')
def add_flight():
	flight_id = request.GET.flight_id.strip()
	company = request.GET.company.strip()
	plane_type = request.GET.plane_type.strip()
	departure_airport = request.GET.departure_airport.strip()
	arrival_airport = request.GET.arrival_airport.strip()
	departure_time = request.GET.departure_time.strip()
	arrival_time = request.GET.arrival_time.strip()
	tourist_reserved = request.GET.tourist_reserved.strip()
	first_reserved = request.GET.first_reserved.strip()
	tourist_price = request.GET.tourist_price.strip()
	first_price = request.GET.first_price.strip()

	result = insert_flight(flight_id, company, plane_type, departure_airport, arrival_airport,
	departure_time, arrival_time, tourist_reserved, first_reserved, tourist_price, first_price)
	if result:
		message = "航班信息插入成功！"
	else:
		message = "航班信息插入失败！"

	return template('administrator', rows = query_flight(), message = message)

#机场信息添加操作
@route('/add_airport', method='GET')
def add_airport():
	airport = request.GET.airport.strip()
	city = request.GET.city.strip()

	result = insert_airport(airport, city)
	if result:
		message = "机场信息插入成功！"
	else:
		message = "机场信息插入失败！"

	return template('airport', rows = query_airport(), message = message)

#机型信息添加操作
@route('/add_plane_type', method='GET')
def add_plane_type():
	plane_type = request.GET.type.strip()
	tourist_class = request.GET.tourist_class.strip()
	first_class = request.GET.first_class.strip()

	result = insert_plane_type(plane_type, tourist_class, first_class)
	if result:
		message = "机型信息插入成功！"
	else:
		message = "机型信息插入失败！"

	return template('plane_type', rows = query_plane_type(), message = message)

#航班信息删除操作
@route('/remove_flight/<flight_id>', method='GET')
def remove_flight(flight_id):
	result = delete_flight(flight_id)
	if result:
	 	message = "航班信息删除成功！"
	else:
		message = "航班信息删除失败！"

	return template('administrator', rows = query_flight(), message = message)

#机场信息删除操作
@route('/remove_airport/<airport>', method='GET')
def remove_airport(airport):
	result = delete_airport(airport)
	if result:
	 	message = "机场信息删除成功！"
	else:
		message = "机场信息删除失败！"

	return template('airport', rows = query_airport(), message = message)

#机型信息删除操作
@route('/remove_plane_type/<plane_type>', method='GET')
def remove_plane_type(plane_type):
	result = delete_plane_type(plane_type)
	if result:
	 	message = "机型信息删除成功！"
	else:
		message = "机型信息删除失败！"

	return template('plane_type', rows = query_plane_type(), message = message)

#航班信息修改界面，输入要修改的信息
@route('/modify_flight/<flight_id>')
def modify_flight(flight_id):
	return template('modify_flight', flight_id = flight_id , message = ' ')

#航班信息修改操作
@route('/modify_flight/<old_flight_id>', method = 'POST')
def modify_flight(old_flight_id):
	flight_id = request.forms.get('flight_id')
	company = request.forms.get('company')
	plane_type = request.forms.get('plane_type')
	departure_airport = request.forms.get('departure_airport')
	arrival_airport = request.forms.get('arrival_airport')
	departure_time = request.forms.get('departure_time')
	arrival_time = request.forms.get('arrival_time')
	tourist_reserved = request.forms.get('tourist_reserved')
	first_reserved = request.forms.get('first_reserved')
	tourist_price = request.forms.get('tourist_price')
	first_price = request.forms.get('first_price')

	result = update_flight_all(old_flight_id, flight_id, company, plane_type, departure_airport, arrival_airport,
	departure_time, arrival_time, tourist_reserved, first_reserved, tourist_price, first_price)

	if result:
		message = "航班信息修改成功！"
	else:
		message = "航班信息修改失败！"

	return template('administrator', rows = query_flight(), message = message)

#机场信息修改界面，输入要修改的信息
@route('/modify_airport/<airport>')
def modify_airport(airport):
	return template('modify_airport', airport = airport , message = ' ')

#机场信息修改操作
@route('/modify_airport/<old_airport>', method = 'POST')
def modify_airport(old_airport):
	airport = request.forms.get('airport')
	city = request.forms.get('city')

	result = update_airport(old_airport, airport, city)

	if result:
		message = "机场信息修改成功！"
	else:
		message = "机场信息修改失败！"

	return template('airport', rows = query_airport(), message = message)

#机型信息修改界面，输入要修改的信息
@route('/modify_plane_type/<plane_type>')
def modify_plane_type(plane_type):
	return template('modify_plane_type', plane_type = plane_type , message = ' ')

#机型信息修改操作
@route('/modify_plane_type/<old_plane_type>', method = 'POST')
def modify_plane_type(old_plane_type):
	plane_type = request.forms.get('type')
	tourist_class = request.forms.get('tourist_class')
	first_class = request.forms.get('first_class')

	result = update_plane_type(old_plane_type, plane_type, tourist_class, first_class)
	if result:
		message = "机型信息修改成功！"
	else:
		message = "机型信息修改失败！"

	return template('plane_type', rows = query_plane_type(), message = message)

#管理员为已付款旅客打印订单
@route('/print_order/<pass_id>/<flight_id>')
def print_order(pass_id, flight_id):
	#首先查询该机票是否已经打印
	if is_printed(pass_id, flight_id):
		message = "机票已经打印，打印失败！"
	else:
		#再查询旅客是否已经付款，若未付款则不能打印
		if not is_paid(pass_id, flight_id):
			message = "机票还未付款，打印失败！"
		else:
			result = update_ticket(pass_id, flight_id, 'print')
			if result:
				message = "机票打印成功！"
			else:
				message = "机票打印失败！"
	result = query_ticket()

	return template('maintain_order', rows = result, message = message)

#计算航班的满座率
@route('/calcul_full/<flight_id>/<plane_type>')
def calcul_full(flight_id, plane_type):
	#首先查到已预订的座位数
	result0 = query_flight_seat(flight_id)
	tourist_reserved = result0[0]
	first_reserved = result0[1]
	#再查找总的座位数
	result1 = query_plane_type("seat", plane_type)
	tourist_class = result1[0]
	first_class = result1[1]

	tourist_rate = tourist_reserved / tourist_class
	first_rate = first_reserved / first_class		

	message = "经济舱满座率  %.2f%%\\n头等舱满座率 %.2f%%" %(tourist_rate, first_rate)
	return template('administrator', rows = query_flight(), message = message)

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