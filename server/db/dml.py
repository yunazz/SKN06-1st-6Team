import pymysql
import json
from pprint import pprint
from db.sql_query import SQL_INSERT_CAR, SQL_INSERT_CITY

def insert_rows():
    with open('server/crawling/data/city.json', 'r', encoding='utf-8') as f:
        cities = json.load(f)
    with open('server/crawling/data/car.json', 'r', encoding='utf-8') as f:
        cars = json.load(f)
        
    with pymysql.connect(host="127.0.0.1", port=3306, user="team06", password="playdata06", db="project_01") as conn:
        with conn.cursor() as cursor:
            # INSERT City
            for city in cities:
                city_name = city.get("city_name")
                state = city.get("state")
                city_phone = city.get("city_phone")
                city_dpt = city.get("city_dpt")
 
                # INSERT 쿼리 작성 및 실행
                cursor.execute(SQL_INSERT_CITY, (state, city_name, city_phone, city_dpt))
                
        conn.commit()
        
        with conn.cursor() as cursor:
        # INSERT Car
            for car in cars:
                print(car)
                print(car.get("car_type"))
                car_type = car.get("car_type")
                car_name = car.get("car_name")
                maker = car.get("maker")
                national_subsidy = car.get("national_subsidy")

                # INSERT 쿼리 작성 및 실행
                cursor.execute(SQL_INSERT_CAR, (car_type, car_name, maker, national_subsidy))
                    
            conn.commit()
        
    return

    
if __name__ == "__main__":
    insert_rows()