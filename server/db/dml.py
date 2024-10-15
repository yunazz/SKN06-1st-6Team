import pymysql
import json
from datetime import datetime
from db.sql_query import SQL_INSERT_CAR, SQL_INSERT_CITY, SQL_INSERT_SUBSIDY

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
            _unique_car = set() 
    
            for car in cars:
                _unique_car.add((car['maker'], car['car_name'],  car['car_type'],  car['national_subsidy']))
                
            unique_car = [{'maker': maker, 'car_name': car_name, 'car_type': car_type, 'national_subsidy': national_subsidy} for maker, car_name,car_type,national_subsidy in _unique_car]
        
        # INSERT Car
            for car in unique_car:
                
                car_type = car.get("car_type")
                car_name = car.get("car_name")
                maker = car.get("maker")
                national_subsidy = car.get("national_subsidy")

                # INSERT 쿼리 작성 및 실행
                cursor.execute(SQL_INSERT_CAR, (car_type, car_name, maker, national_subsidy))
                
        conn.commit()
        
        with conn.cursor(pymysql.cursors.DictCursor) as cursor:
        # INSERT Subsidy        
            cursor.execute('SELECT city_id, city_name, state from city')
            city_rows = cursor.fetchall()
            cursor.execute('SELECT car_id, car_name from car')
            car_rows = cursor.fetchall()
            
            subsidy_to_insert = []

            for subsidy in cars:
                city_name = subsidy.get("city_name")
                state = subsidy.get("state")
                city_subsidy = float(subsidy.get("city_subsidy").replace(',',''))
                car_name = subsidy.get("car_name")
                print(city_subsidy)
                
                city_id = None
                car_id = None
                
                for city in city_rows:
                    if city['state'] == state and city['city_name'] == city_name:
                        city_id = city['city_id']
                        
                        break 
                    
                for car in car_rows:
                    if car['car_name'] == car_name :
                        car_id = car['car_id']
                        break     
                    

                if city_id is not None and car_id is not None:
                    subsidy_to_insert.append((datetime.today().year, city_subsidy, city_id, car_id))
            
            cursor.executemany(SQL_INSERT_SUBSIDY, subsidy_to_insert)
            
        conn.commit()
    return


if __name__ == "__main__":
    insert_rows()