from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json
import os

def crawling_tel():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    url = 'https://ev.or.kr/nportal/buySupprt/initSubsidyPaymentCheckAction.do'
    driver.get(url)
    driver.maximize_window()

    # 페이지 로드 대기
    wait = WebDriverWait(driver, 10)

    try:
        # 'btnLocalPhone' 버튼 찾기
        button = driver.find_element(By.ID, 'btnLocalPhone')

        # JavaScript로 클릭
        driver.execute_script("arguments[0].click();", button)
        time.sleep(2)

        # 새 창으로 전환
        driver.switch_to.window(driver.window_handles[-1])
        time.sleep(2)

        # CSS 셀렉터 설정
        state_selector = "body > div:nth-child(9) > table > tbody > tr > td:nth-child(1)"
        city_selector = "body > div:nth-child(9) > table > tbody > tr > td:nth-child(2)"
        dep_selector = "body > div:nth-child(9) > table > tbody > tr > td:nth-child(3)"
        tel_selector = "body > div:nth-child(9) > table > tbody > tr > td:nth-child(4)"

        # 크롤링 함수 정의
        def crawling():
            state, city, dep, tel = [], [], [], []
            last_height = driver.execute_script("return document.body.scrollHeight")

            while True:
                # 차종, 제조사, 모델명, 보조금 정보 수집
                states = driver.find_elements(By.CSS_SELECTOR, state_selector)
                cities = driver.find_elements(By.CSS_SELECTOR, city_selector)
                deps = driver.find_elements(By.CSS_SELECTOR, dep_selector)
                tels = driver.find_elements(By.CSS_SELECTOR, tel_selector)

                # 리스트에 추가
                state.extend([i.text for i in states])
                city.extend([i.text for i in cities])
                dep.extend([i.text for i in deps])
                tel.extend([i.text for i in tels])

                # 페이지 끝까지 스크롤
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(3)  # 스크롤 후 데이터를 로드할 시간을 충분히 줍니다

                # 새로운 높이를 가져와 비교, 더 이상 데이터가 없을 때 탈출
                new_height = driver.execute_script("return document.body.scrollHeight")
                if new_height == last_height:
                    break
                last_height = new_height

            return state, city, dep, tel

        # 크롤링 실행
        state, city, dep, tel = crawling()

        # 수집한 정보를 저장
        all_data = []
        for st, ct, de, t in zip(state, city, dep, tel):
            all_data.append({
                'state': st,
                'city_name': ct,
                'city_dpt': de,
                'city_phone': t
            })

        # 현재 창 닫기
        driver.close()
        time.sleep(1)  # 창을 닫고 나서 약간의 시간 대기


        # 수집한 정보를 텍스트 파일로 저장
        os.makedirs('server/crawling/data', exist_ok=True)
        with open('server/crawling/data/city.json', 'w', encoding='utf-8') as file:
            json.dump(all_data, file, ensure_ascii=False, indent=4)
        
        # with open('server/crawling/data/city.py', 'w', encoding='utf-8') as file: # (2)
        #     # 컬럼명 (1)
        #     file.write("시도,")
        #     file.write("지역구분,")
        #     file.write("부서,")
        #     file.write("연락처\n")
        #     # 데이터 삽입
        #     for data in all_data:
        #         file.write(f"{data['시도']},")
        #         file.write(f"{data['지역구분']},")
        #         file.write(f"{data['부서']},")
        #         file.write(f"{data['연락처']}\n")

        # print("크롤링 완료! 데이터가 city.csv에 저장되었습니다.")

    except Exception as e:
        print(f"오류 발생: {e}")

    finally:
        # 드라이버 종료
        driver.quit()
        
        return 'city.json'

if __name__ == "__main__":
    crawling_tel()