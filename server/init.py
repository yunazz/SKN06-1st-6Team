from db.ddl import create_tables
from db.dml import insert_rows
from crawling.subsidy import crawling_subsidy
from crawling.city import crawling_city

if __name__ == '__main__':
    print('DB setting 시작')
    
    # try:
    print('DB setting 1')
    create_tables()
    
    # 크롤링 시간이 오래 걸려 미리 만들어 놓은 /crawling/data/*.json 참조하기 위해 주석처리
    # crawling_subsidy() 
    # crawling_tel()
    
    insert_rows()
        # print('DB setting 2')
        
        # subsidy = get_subsidy()
        # insert_rows(subsidy)
        
        # print('DB setting 완료')
    # except:
    #     print('DB setting 오류')
    