import pymysql
from db.sql_query import SQL_CREATE_TB_CAR, SQL_CREATE_TB_SUBSIDY, SQL_CREATE_TB_CITY
# import pandas as pd 

def create_DB(password):
    with pymysql.connect(host="localhost", port=3306, user="root", password=password) as conn:
        with conn.cursor() as cursor:
            # CREATE DATABASE
            cursor.execute("DROP DATABASE IF EXISTS SKN06_6Team")
            cursor.execute('CREATE DATABASE SKN06_6Team')
            
            cursor.execute(f"CREATE USER 'team06'@'localhost' IDENTIFIED BY '{password}'")
            cursor.execute(f"GRANT ALL PRIVILEGES ON *.* TO 'team06'@'localhost' WITH GRANT OPTION")
            cursor.execute(f"CREATE USER 'team06'@'%' IDENTIFIED BY '{password}';")
            cursor.execute(f"GRANT ALL PRIVILEGES ON *.* TO 'team06'@'%' WITH GRANT OPTION")

            cursor.execute("FLUSH PRIVILEGES")

def create_tables(password):
    with pymysql.connect(host="localhost", port=3306, user="team06", password=password, db="SKN06_6Team") as conn:
        with conn.cursor() as cursor:
            # CREATE TABLE
            cursor.execute("DROP TABLE IF EXISTS car") 
            cursor.execute("DROP TABLE IF EXISTS subsidy") 
            cursor.execute("DROP TABLE IF EXISTS city") 
            
            cursor.execute(SQL_CREATE_TB_CAR)
            cursor.execute(SQL_CREATE_TB_SUBSIDY)
            cursor.execute(SQL_CREATE_TB_CITY)