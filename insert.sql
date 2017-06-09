insert into passenger values(1001, '李伟光', 132),
	(1003, '张三', 133),
	(1004, '李四', 186),
	(1005, '王五', 188);

insert into flight values(1, '东方航空', '波音737', '天河机场', '浦东机场', '2017-9-2 13:00:00', '2017-9-2 15:00:00', 0, 0, 600, 1000);

insert into flight values(2, '南方航空', '空客A380', '浦东机场', '旧金山机场', '2017-8-12 16:00:00', '2017-8-12 17:00:00', 0, 0, 6600, 20000);

insert into airport values('天河机场', '武汉'),
	('浦东机场', '上海'),
	('虹桥机场', '上海'),
	('旧金山机场', '旧金山');

insert into plane_type values('波音737', 400, 50),
	('空客A320', 600, 100),
	('空客A380', 700, 150);

select airport from airport
where city = '上海';

select company, id, departure_time, arrival_time, departure_airport, arrival_airport, tourist_price
from flight
where departure_airport in
	(select airport
	from airport
	where city = '武汉'
	)
	and arrival_airport in
	(select airport
	from airport
	where city = '上海'
	)
	and DATE_FORMAT(departure_time, '%Y-%m-%d') = '2017-09-02';

select pname, pass_id, cellnumber, flight_id, class, printed, paid
from passenger, ticket
where pass_id = passenger.id 

insert into ticket
	values(1003, 1, '头等舱', 1000, 0, 0)