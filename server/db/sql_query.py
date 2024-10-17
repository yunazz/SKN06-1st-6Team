SQL_CREATE_TB_CAR = '''
CREATE TABLE car (  
    car_id int unsigned auto_increment primary key,
    car_type varchar(10) not null,
    car_name varchar(50) not null unique,
    maker varchar(20) not null,
    national_subsidy DECIMAL(11, 0) default 0.00 not null,
    passenger_cnt varchar(10),
    max_speed varchar(30),
    range_per_charge varchar(30),
    battery varchar(30),
    maker_phone varchar(13),
    maker_nation varchar(20)
) 
'''
    
SQL_CREATE_TB_SUBSIDY = '''
CREATE TABLE subsidy (  
    subsidy_id int unsigned auto_increment primary key,
    subsidy_year YEAR not null, 
    city_subsidy DECIMAL(11, 0),
    city_id int not null,
    car_id int not null
) 
'''

SQL_CREATE_TB_CITY = '''
CREATE TABLE city (  
    city_id int unsigned auto_increment primary key,
    state varchar(20) not null,
    city_name varchar(20) not null,
    city_dpt varchar(20),
    city_phone varchar(15)
) 
'''

SQL_INSERT_CAR = 'INSERT INTO car (car_type, car_name, maker, national_subsidy) values (%s, %s, %s,%s)'

SQL_INSERT_CITY = 'INSERT INTO city (state, city_name, city_phone, city_dpt) values (%s, %s, %s,%s)'

SQL_INSERT_SUBSIDY  = 'INSERT INTO subsidy (subsidy_year, city_subsidy, city_id, car_id) values (%s, %s, %s, %s)'

SQL_UPDATE_CAR_DETAIL = '''
UPDATE car SET 
    passenger_cnt = %s, 
    max_speed = %s, 
    range_per_charge = %s, 
    battery = %s, 
    maker_phone = %s, 
    maker_nation = %s
WHERE car_id = %s;
'''
