SQL_TB_CAR = '''
CREATE TABLE car (  
    car_id int unsigned auto_increment primary key,
    car_type varchar(10) not null,
    car_name varchar(30) not null unique,
    maker varchar(20) not null,
    power_type varchar(3) not null,
    national_subsidy DECIMAL(11, 0) default 0.00 not null
) 
'''
    
SQL_TB_SUBSIDY = '''
CREATE TABLE subsidy (  
    subsidy_id int unsigned auto_increment primary key,
    subsidy_year YEAR not null, 
    subsidy DECIMAL(11, 0),
    city_id int not null,
    power_type varchar(3)
) 
'''

SQL_TB_CITY = '''
CREATE TABLE city (  
    city_id int unsigned auto_increment primary key,
    city_name varchar(20) not null,
    state YEAR not null
) 
'''

SQL_TB_CITY_HALL = '''
CREATE TABLE city_hall (  
    city_hall_id int unsigned auto_increment primary key,
    city_id int not null,
    department varchar(11),
    phone varchar(11)
) 
'''