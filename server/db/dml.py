import pymysql
import json
from pprint import pprint
from db.sql_query import SQL_INSERT_CITY

def insert_rows():
    with open('server/crawling/data/city.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    with pymysql.connect(host="127.0.0.1", port=3306, user="team06", password="playdata06", db="project_01") as conn:
        with conn.cursor() as cursor:
            # INSERT
            for city_data in data:
                city_name = city_data.get("city_name")
                state = city_data.get("state")
                city_phone = city_data.get("city_phone")
                city_dpt = city_data.get("city_dpt")
 
                # INSERT 쿼리 작성 및 실행
                cursor.execute(SQL_INSERT_CITY, (state, city_name, city_phone, city_dpt))
                
        conn.commit()
    return
    
if __name__ == "__main__":
    insert_rows()