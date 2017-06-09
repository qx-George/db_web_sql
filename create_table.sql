create table passenger(
	id varchar(20) primary key,
	pname char(10),
	cellnumber char(15));

create table ticket(
	pass_id varchar(20),
	flight_id varchar(10),
	class char(10) check (class in('经济舱', '头等舱')),
	price smallint check(price > 0),
	printed bool,
	paid bool,
	primary key(pass_id, flight_id),
	foreign key(pass_id) references passenger(id),
	foreign key(flight_id) references flight(id));

create table flight(
	id varchar(10) primary key,
	company varchar(20),
	plane_type varchar(20),
	departure_airport varchar(20),
	arrival_airport varchar(20),
	departure_time datetime,
	arrival_time datetime,
	tourist_reserved smallint unsigned,
	first_reserved smallint unsigned,
	tourist_price smallint check (price > 0),  
	first_price smallint check (price > 0),
	foreign key(plane_type) references plane_type(type),
	foreign key(departure_airport) references airport(airport),
	foreign key(arrival_airport) references airport(airport));

create table airport(
	airport varchar(20) primary key,
	city char(10));   

create table plane_type(
	type varchar(20) primary key,
	tourist_class smallint unsigned,
	first_class smallint unsigned);