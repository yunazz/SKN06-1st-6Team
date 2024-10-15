from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time

# 드라이버 설정 및 URL 이동
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.set_window_size(1280, 800)
url = 'https://ev.or.kr/nportal/buySupprt/initSubsidyTargetVehicleAction.do#'
driver.get(url)

# 페이지 로드 대기
wait = WebDriverWait(driver, 10)

# 수집한 정보를 저장할 리스트
all_data = []

def crawling():
    """현재 페이지에서 전기차 정보를 수집하는 함수"""
    car_name, car_person_num, max_speed, dis_per_charge, battery, sub, phone_num, maker, makerN = [], [], [], [], [], [], [], [], []

    try:
        # 각 요소를 찾을 때 대기 시간을 설정하여 요소가 로드되었는지 확인
        car_names = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".itemCont a h4 p")))
        car_person_nums = driver.find_elements(By.CSS_SELECTOR, ".itemCont a dl dd:nth-child(2)")
        max_speeds = driver.find_elements(By.CSS_SELECTOR, ".itemCont a dl dd:nth-child(3)")
        dis_per_charges = driver.find_elements(By.CSS_SELECTOR, ".itemCont a dl dd:nth-child(4)")
        batterys = driver.find_elements(By.CSS_SELECTOR, ".itemCont a dl dd:nth-child(5)")
        subs = driver.find_elements(By.CSS_SELECTOR, ".itemCont a dl dd:nth-child(6)")
        phone_nums = driver.find_elements(By.CSS_SELECTOR, ".itemCont a dl dd:nth-child(7)")
        makers = driver.find_elements(By.CSS_SELECTOR, ".itemCont a dl dd:nth-child(8)")
        makerNs = driver.find_elements(By.CSS_SELECTOR, ".itemCont a dl dd:nth-child(9)")

        # 데이터를 리스트에 저장
        if car_names:
            car_name.extend([i.text for i in car_names])
            car_person_num.extend([i.text for i in car_person_nums])
            max_speed.extend([i.text for i in max_speeds])
            dis_per_charge.extend([i.text for i in dis_per_charges])
            battery.extend([i.text for i in batterys])
            sub.extend([i.text for i in subs])
            phone_num.extend([i.text for i in phone_nums])
            maker.extend([i.text for i in makers])
            makerN.extend([i.text for i in makerNs])
        else:
            print("데이터가 없습니다.")
            return None

    except TimeoutException:
        print("데이터 로드 시간 초과.")
        return None

    return car_name, car_person_num, max_speed, dis_per_charge, battery, sub, phone_num, maker, makerN

def go_to_next_page():
    """다음 페이지로 이동하는 함수"""
    try:
        # 다음 페이지 버튼을 찾고 클릭
        next_button = driver.find_element(By.CSS_SELECTOR, "#pageingPosition > a.next.arrow")
        next_button.click()
        time.sleep(2)  # 페이지 로드 대기
        return True
    except NoSuchElementException:
        print("다음 페이지가 없습니다.")
        return False

def fetch_data(company_name):
    """지정한 회사의 정보를 크롤링하는 함수"""
    try:
        # 'schCompany' 드롭다운에서 제조사 선택
        dropdown = Select(driver.find_element(By.ID, 'schCompany'))
        dropdown.select_by_visible_text(company_name)
        time.sleep(2)  # Allow dropdown to update

        # 검색 버튼 클릭
        search_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="searchForm"]/div/table/tbody/tr[4]/td/button')))
        search_button.click()
        time.sleep(3)  # 페이지 로드 대기

        # 첫 페이지부터 데이터를 수집하고, 다음 페이지가 있으면 반복
        previous_data_count = -1
        while True:
            # 현재 페이지 데이터 수집
            car_data = crawling()

            # 수집한 데이터가 없으면 종료
            if not car_data:
                break

            car_name, car_person_num, max_speed, dis_per_charge, battery, sub, phone_num, maker, makerN = car_data

            # 중복 없이 새로운 데이터를 수집
            for cn, cpn, ms, dpc, ba, sb, pn, ma, maN in zip(car_name, car_person_num, max_speed, dis_per_charge, battery, sub, phone_num, maker, makerN):
                if cn and {'차종': cn, '승차인원': cpn, '최고속도출력': ms, '1회충전주행거리': dpc, '배터리': ba, '국고보조금': sb, '판매사연락처': pn, '제조사': ma, '제조국가': maN} not in all_data:
                    all_data.append({
                        '차종': cn,
                        '승차인원': cpn,
                        '최고속도출력': ms,
                        '1회충전주행거리': dpc,
                        '배터리': ba,
                        '국고보조금': sb,
                        '판매사연락처': pn,
                        '제조사': ma,
                        '제조국가': maN
                    })

            # 수집된 데이터의 개수가 변하지 않으면 마지막 페이지로 간주하고 종료
            current_data_count = len(all_data)
            if current_data_count == previous_data_count:
                break
            previous_data_count = current_data_count

            # 다음 페이지로 이동 시도
            if not go_to_next_page():
                break

    except Exception as e:
        print(f"{company_name} 정보 크롤링 중 오류 발생: {e}")

# 제조사 목록
companies = ["기아", "마이브", "메르세데스벤츠코리아", "볼보자동차코리아", "스텔란티스코리아", "쎄보모빌리티", "케이지모빌리티", "테슬라코리아", "폭스바겐그룹코리아", "폴스타오토모티브코리아", "한국토요타자동차", "현대자동차", "BMW"]

# 각 제조사에 대해 데이터 수집
for company in companies:
    fetch_data(company)

# 수집한 정보를 JSON 파일로 저장
os.makedirs('server/crawling/data', exist_ok=True)
with open('server/crawling/data/cardetail.json', 'w', encoding='utf-8') as file:
    json.dump(all_data, file, ensure_ascii=False, indent=4)

print("크롤링 완료! 데이터가 car_data.txt에 저장되었습니다.")

# 드라이버 종료
driver.quit()
