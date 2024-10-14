
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json
import os

def crawling_subsidy():
    # 드라이버 설정 및 URL 이동
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    url = 'https://ev.or.kr/nportal/buySupprt/initSubsidyPaymentCheckAction.do'
    driver.get(url)
    driver.maximize_window()

    # 페이지 로드 대기
    wait = WebDriverWait(driver, 10)

    try:
        # 'btnLocalCarPrc' 버튼 찾기
        button = wait.until(EC.element_to_be_clickable((By.ID, 'btnLocalCarPrc')))

        # 해당 요소가 보이도록 스크롤
        driver.execute_script("arguments[0].scrollIntoView(true);", button)
        time.sleep(1)  # 잠시 대기하여 스크롤 후 안정화

        # JavaScript로 클릭
        driver.execute_script("arguments[0].click();", button)

        # 새 창으로 전환
        WebDriverWait(driver, 10).until(lambda driver: len(driver.window_handles) > 1)
        driver.switch_to.window(driver.window_handles[-1])
        time.sleep(2)

        # 시/도, 지역구분 CSS 셀렉터 설정
        state_selector = "body > form > div > table > tbody > tr > td:nth-child(1)"
        city_selector = "body > form > div > table > tbody > tr > td:nth-child(2)"

        # 시도 및 지역구분 정보 크롤링
        states = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, state_selector)))
        cities = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, city_selector)))

        # 시도와 지역구분 텍스트 저장
        state_list = [state.text for state in states]
        city_list = [city.text for city in cities]

        # 수집한 정보를 저장할 리스트
        all_data = []

        # 모든 지역에 대해 조회 버튼 클릭
        for i in range(len(state_list)):
            # 각 지역의 조회 버튼 클릭
            button = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, f'body > form > div > table > tbody > tr:nth-child({i + 1}) > td.tr_car_btn > a')))

            # 해당 요소가 보이도록 스크롤
            driver.execute_script("arguments[0].scrollIntoView(true);", button)
            time.sleep(1)  # 잠시 대기하여 스크롤 후 안정화

            # JavaScript로 클릭
            driver.execute_script("arguments[0].click();", button)

            # 새 창으로 전환
            WebDriverWait(driver, 10).until(lambda driver: len(driver.window_handles) > 1)
            driver.switch_to.window(driver.window_handles[-1])
            time.sleep(2)

            # CSS 셀렉터 설정
            car_type_selector = "body > form > div > table > tbody > tr > td:nth-child(1)"
            maker_selector = "body > form > div > table > tbody > tr > td:nth-child(2)"
            model_selector = "body > form > div > table > tbody > tr > td:nth-child(3)"
            subN_selector = "body > form > div > table > tbody > tr > td:nth-child(4)"
            subC_selector = "body > form > div > table > tbody > tr > td:nth-child(5)"
            subALL_selector = "body > form > div > table > tbody > tr > td:nth-child(6)"

            # 크롤링 함수 정의
            def crawling():
                car_type, maker, model, subN, subC, subALL = [], [], [], [], [], []
                last_height = driver.execute_script("return document.body.scrollHeight")

                while True:
                    # 차종, 제조사, 모델명, 보조금 정보 수집
                    car_types = driver.find_elements(By.CSS_SELECTOR, car_type_selector)
                    makers = driver.find_elements(By.CSS_SELECTOR, maker_selector)
                    models = driver.find_elements(By.CSS_SELECTOR, model_selector)
                    subNs = driver.find_elements(By.CSS_SELECTOR, subN_selector)
                    subCs = driver.find_elements(By.CSS_SELECTOR, subC_selector)
                    subALLs = driver.find_elements(By.CSS_SELECTOR, subALL_selector)

                    # 리스트에 추가
                    car_type.extend([i.text for i in car_types])
                    maker.extend([i.text for i in makers])
                    model.extend([i.text for i in models])
                    subN.extend([i.text for i in subNs])
                    subC.extend([i.text for i in subCs])
                    subALL.extend([i.text for i in subALLs])

                    # 페이지 끝까지 스크롤
                    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    time.sleep(3)  # 스크롤 후 데이터를 로드할 시간을 충분히 줍니다

                    # 새로운 높이를 가져와 비교, 더 이상 데이터가 없을 때 탈출
                    new_height = driver.execute_script("return document.body.scrollHeight")
                    if new_height == last_height:
                        break
                    last_height = new_height

                return car_type, maker, model, subN, subC, subALL

            # 크롤링 실행
            car_type, maker, model, subN, subC, subALL = crawling()

            # 수집한 정보를 저장
            for ct, mk, mdl, sn, sc, sa in zip(car_type, maker, model, subN, subC, subALL):
                all_data.append({
                    'car_type': ct,
                    'maker': mk,
                    'car_name': mdl,
                    'national_subsidy': sn,
                    'city_subcsidy': sc,
                    'state': state_list[i],
                    'city': city_list[i]
                })

            # 현재 창 닫기
            driver.close()
            time.sleep(1)  # 창을 닫고 나서 약간의 시간 대기
            # 이전 창으로 전환
            driver.switch_to.window(driver.window_handles[-1])



        os.makedirs('server/crawling/data', exist_ok=True)
        with open('server/crawling/data/car_subsidy.json', 'w', encoding='utf-8') as file: # (2)
            json.dump(all_data, file, ensure_ascii=False, indent=4)
        
            
        # 수집한 정보를 텍스트 파일로 저장
        # os.makedirs('server/crawling/data', exist_ok=True)
        # with open('server/crawling/data/car_subsidy.csv', 'w', encoding='utf-8') as file: # (2)
        #     # 컬럼명 (1)
        #     file.write("시도,")
        #     file.write("지역구분,")
        #     file.write("차종,")
        #     file.write("제조사,")
        #     file.write("모델명,")
        #     file.write("보조금(국비),")
        #     file.write("보조금(지방비),")
        #     file.write("보조금,\n")
        #     # data 삽입
        #     for data in all_data:
        #         file.write(f"{data['시도']},")
        #         file.write(f"{data['지역구분']},")
        #         file.write(f"{data['차종']},")
        #         file.write(f"{data['제조사']},")
        #         file.write(f"{data['모델명']},")
        #         file.write(f"{data['보조금(국비)']},")
        #         file.write(f"{data['보조금(지방비)']},")
        #         file.write(f"{data['보조금']}\n")

        # print("크롤링 완료! 데이터가 subsidy_data.csv에 저장되었습니다.")

    except Exception as e:
        print(f"오류 발생: {e}")

    finally:
        # 드라이버 종료
        driver.quit()
    return 'subsidy_data.json' # (2)



if __name__ == "__main__":
    crawling_subsidy()