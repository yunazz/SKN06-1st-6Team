from db.ddl import create_DB, create_tables
from db.dml import insert_rows
from crawling.subsidy import crawling_subsidy
from crawling.city import crawling_city
from crawling.car_detail import crawling_car_detail

if __name__ == '__main__':
    print('DB setting 시작')
    
    try:
        print('DB setting 1')
        # create_tables()
        print('mySQL의 root user 비밀번호를 입력해주세요')
        password = input()
        create_DB(password)
        create_tables(password)
        # 크롤링 시간이 오래 걸려 미리 만들어 놓은 /crawling/data/*.json 참조하기 위해 주석처리
        # crawling_subsidy() 
        # crawling_city()
        # crawling_car_detail()
        
        insert_rows()
    except:
        print('DB setting 오류')
    