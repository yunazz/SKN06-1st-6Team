import pymysql
import json
from datetime import datetime
from db.sql_query import SQL_INSERT_CAR, SQL_INSERT_CITY, SQL_INSERT_SUBSIDY, SQL_UPDATE_CAR_DETAIL

def insert_rows(password):
    with open('server/crawling/data/city.json', 'r', encoding='utf-8') as f:
        cities = json.load(f)
    with open('server/crawling/data/car.json', 'r', encoding='utf-8') as f:
        cars = json.load(f)
        
    with pymysql.connect(host="localhost", port=3306, user="root", password=password, db="SKN06_6Team") as conn:
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
        
        # INSERT Car
        with conn.cursor() as cursor:
            _unique_car = set() 
    
            for car in cars:
                _unique_car.add((car['maker'], car['car_name'],  car['car_type'],  car['national_subsidy']))

            unique_car = [{'maker': maker, 'car_name': car_name, 'car_type': car_type, 'national_subsidy': national_subsidy} for maker, car_name,car_type,national_subsidy in _unique_car]
        
            for car in unique_car:
                car_type = car.get("car_type")
                car_name = car.get("car_name")
                maker = car.get("maker")
                national_subsidy = car.get("national_subsidy")

                # INSERT 쿼리 작성 및 실행
                cursor.execute(SQL_INSERT_CAR, (car_type, car_name, maker, national_subsidy))
                
        conn.commit()
        
        # INSERT Subsidy        
        with conn.cursor(pymysql.cursors.DictCursor) as cursor:
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

        # INSERT Car details     
        with conn.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute('SELECT car_id, car_name from car')
            car_rows = cursor.fetchall()
            
            details_to_insert = []
            for car in cars:
                passenger_cnt = car.get("passenger_cnt").replace('- 승차인원:','')
                max_speed = car.get("max_speed").replace('- 최고속도출력:','')
                range_per_charge = car.get("range_per_charge").replace('- 1회충전주행거리 :','')
                battery = car.get("battery").replace('- 배터리 :','')
                maker_phone = car.get("maker_phone").replace('- 판매사연락처 :','')
                maker_nation = car.get("maker_nation").replace('- 제조국가 :','')
                
                car_id = None
                    
                for car in car_rows:
                    if car['car_name'] == car_name :
                        car_id = car['car_id']
                        break     

                if car_id is not None:
                    subsidy_to_insert.append((passenger_cnt, max_speed, range_per_charge, battery, maker_phone, maker_nation, car_id))
            print(details_to_insert)
            cursor.executemany(SQL_UPDATE_CAR_DETAIL, details_to_insert)
            
        conn.commit()
    return


if __name__ == "__main__":
    insert_rows()