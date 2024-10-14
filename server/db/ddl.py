import pymysql
from db.sql_query import SQL_TB_CAR, SQL_TB_SUBSIDY, SQL_TB_CITY
# import pandas as pd 

def create_tables():
    with pymysql.connect(host="127.0.0.1", port=3306, user="team06", password="playdata06", db="project_01") as conn:
        with conn.cursor() as cursor:
            # CREATE TABLE
            cursor.execute("DROP TABLE IF EXISTS car") 
            cursor.execute("DROP TABLE IF EXISTS subsidy") 
            cursor.execute("DROP TABLE IF EXISTS city") 
            
            cursor.execute(SQL_TB_CAR)
            cursor.execute(SQL_TB_SUBSIDY)
            cursor.execute(SQL_TB_CITY)