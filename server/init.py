from db.ddl import create_DB, create_tables
from db.dml import insert_rows
from crawling.subsidy import crawling_subsidy
from crawling.city import crawling_city

if __name__ == '__main__':
    print('DB setting 시작')
    
    # try:
    print('DB setting 1')
    print('mySQL의 root 계정 비밀번호를 입력해주세요.')
    password = input()
    create_DB(password)
    create_tables(password)
    
    # crawling_subsidy()
    # crawling_tel()
    insert_rows()
        # print('DB setting 2')
        
        # subsidy = get_subsidy()
        # insert_rows(subsidy)
        
        # print('DB setting 완료')
    # except:
    #     print('DB setting 오류')
    