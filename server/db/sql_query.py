SQL_DB = '''
CREATE DATABASE SKN06_6Team
'''

SQL_TB_CAR = '''
CREATE TABLE car (  
    car_id int unsigned auto_increment primary key,
    car_type varchar(10) not null,
    car_name varchar(30) not null unique,
    maker varchar(20) not null,
    national_subsidy DECIMAL(11, 0) default 0.00 not null
) 
'''
    
SQL_TB_SUBSIDY = '''
CREATE TABLE subsidy (  
    subsidy_id int unsigned auto_increment primary key,
    subsidy_year YEAR not null, 
    subsidy DECIMAL(11, 0),
    city_id int not null
) 
'''

SQL_TB_CITY = '''
CREATE TABLE city (  
    city_id int unsigned auto_increment primary key,
    state varchar(20) not null,
    city_name varchar(20) not null,
    city_dpt varchar(20),
    city_phone varchar(15)
) 
'''

SQL_INSERT_CAR = 'INSERT INTO car (car_type, car_name, maker, national_subsidy) values(%s, %s, %s,%s)'

SQL_INSERT_CITY = 'INSERT INTO city (state, city_name, city_phone, city_dpt) values(%s, %s, %s,%s)'