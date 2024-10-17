import streamlit as st
import pandas as pd
import pymysql
from sqlalchemy import create_engine

## 화면 설정
title = "🏆 전국 전기차 보조금 비교"
st.set_page_config(page_title=title,page_icon="🏆",layout="wide",)
st.title(title)
st.markdown(
    "최근 우리나라는 자동차 업계에 전기자동자 분야가 급부상하면서 소비자들의 구매욕구가 증가중입니다."
    "그러나, 증가하는 수요와 다르게 보조금 지원 조회가 복잡하고 차량정보 또한 한번에 찾을 수 있는 프로그램이 없었습니다."
    "그래서 국내 존재하는 차량 브랜드들의 전기차 정보와 지역별 보조금 정보를 한번에 확인할 수 있는 통합 검색 애플리케이션을 구축하였습니다."
)
st.divider()

## DB 연결
with st.popover("login"):
    user = st.text_input("MySQL localhost 유저 이름을 입력해주세요")
    password = st.text_input("비밀번호를 입력해주세요", type = "password")

db_connection_str = f'mysql+pymysql://{user}:{password}@localhost/SKN06_6Team'
engine = create_engine(db_connection_str)

def read_df(query):
    with engine.connect() as conn:
        result = pd.read_sql_query(query, conn)
    return result

## 전체 데이터 불러오기
q = '''SELECT subsidy.subsidy_year AS "연도",
              city.state AS "시도",
              city.city_name AS "지역구분",
              car.car_type AS "차종",
              car.maker AS "판매사",
              car.car_name AS "모델",
              car.passenger_cnt AS "승차인원",
              car.max_speed AS "최고 속력",
              car.range_per_charge AS "1회 충전 주행거리",
              car.battery AS "배터리",
              car.maker_phone AS "판매사 연락처",
              car.maker_nation AS "제조국가",
              car.national_subsidy AS "국고보조금",
              subsidy.city_subsidy  AS "지자체보조금",
              (car.national_subsidy + subsidy.city_subsidy) AS "총 지원금"
        FROM subsidy
             LEFT OUTER JOIN
             car
             ON subsidy.car_id = car.car_id

             LEFT OUTER JOIN
             city
             ON subsidy.city_id = city.city_id;'''
alldf = read_df(q)

## filter 목록 불러오기
# 데이터베이스에서 시도 목록 가져오기
def get_state_names():
    query = 'SELECT DISTINCT state FROM city'
    df = read_df(query)
    return df

# 데이터베이스에서 지역구분 목록 가져오기
def get_city_names(state):
    query = f'SELECT DISTINCT city_name FROM city WHERE state = "{state}"'
    df = read_df(query)
    return df

# 데이터베이스에서 차량 제조사 목록 가져오기
def get_maker_names():
    query = 'SELECT DISTINCT maker FROM car'
    df = read_df(query)
    return df

# 데이터베이스에서 차량 모델 목록 가져오기
def get_model_names(maker):
    query = f'SELECT DISTINCT car_name FROM car WHERE maker = "{maker}"'
    df = read_df(query)
    return df

## 필터 화면 설정
make_filter = st.checkbox("필터 설정")
if make_filter:
    col1, col2 = st.columns(2)
    with col1:
        # 셀렉박스 배치
        state_names = get_state_names()
        state = st.selectbox('시/도를 고르세요',state_names)  # state

        maker_names = get_maker_names()
        maker = st.selectbox('판매사를 고르세요',maker_names) # brand

    with col2:
        city_names = get_city_names(state)
        city = st.selectbox('지역을 고르세요',city_names)  # city

        car_names = get_model_names(maker)
        car = st.selectbox('모델을 고르세요',car_names) # model

    st.divider()

    ## SQL 쿼리 작성
    # 셀렉 박스의 값에 대응하는 SELECT문 작성
    q1 = '''SELECT city.state AS "시도",
               city.city_name AS "지역구분",
               car.maker AS "판매사",
               car.car_name AS "모델",
               car.national_subsidy AS "국고보조금",
               subsidy.city_subsidy  AS "지자체보조금",
               (car.national_subsidy + subsidy.city_subsidy) AS "총 지원금"
        FROM subsidy
             LEFT OUTER JOIN
             car
             ON subsidy.car_id = car.car_id

             LEFT OUTER JOIN
             city
             ON subsidy.city_id = city.city_id
        WHERE city.city_name = "{}" AND car.car_name = "{}"'''
    q1 = q1.format(city, car)
    # 셀렉 박스의 지역의 연락처를 조회하는 SELECT문 작성
    q2 = '''SELECT city_name AS "지역구분",
                   city_dpt AS "부서",
                   city_phone AS "연락처"
            FROM city
            WHERE city_name = "{}"'''
    q2 = q2.format(city)

    # 셀렉 박스의 모델의 전 지역 보조금을 조회하는 SELECT문 작성
    q3 = '''SELECT city.state AS "시도",
                   city.city_name AS "지역구분",
                   car.national_subsidy AS "국고보조금",
                   subsidy.city_subsidy  AS "지자체보조금",
                   (car.national_subsidy + subsidy.city_subsidy) AS "총 지원금"
             FROM subsidy
                  LEFT OUTER JOIN
                  car
                  ON subsidy.car_id = car.car_id

                  LEFT OUTER JOIN
                  city
                  ON subsidy.city_id = city.city_id
             WHERE car.car_name = "{}"
             ORDER BY (car.national_subsidy + subsidy.city_subsidy) DESC'''
    q3 = q3.format(car)
    # 차량 정보를 조회하는 select문 작성
    q4 = '''SELECT DISTINCT car_name AS "모델",
                   maker AS "판매사",
                   passenger_cnt AS "승차인원",
                   max_speed AS "최고속력",
                   range_per_charge AS "1회 충전 주행거리",
                   battery AS "배터리",
                   maker_phone AS "판매사 연락처",
                   maker_nation AS "제조국가"
            FROM car
            WHERE car_name = "{}"'''
    q4 = q4.format(car)

    sub = read_df(q1)
    phone = read_df(q2)
    total = read_df(q3)
    detail = read_df(q4)

    col3, col4 = st.columns([0.6, 0.4])
    with col3:
        st.markdown(f"{city}에서 {car}를 구매할 때 받을 수 있는 지원금")
        st.dataframe(sub, use_container_width=True, hide_index=True)
        st.divider()
        st.markdown(f"{car}의 기타 지역 지원금")
        st.dataframe(total, use_container_width=True, hide_index=True)
    with col4:
        st.markdown(f"{city}의 관할 부서 연락처")
        st.dataframe(phone, use_container_width=True, hide_index=True)
        st.divider()
        st.markdown(f"{car}의 정보")
        st.dataframe(detail.transpose(), use_container_width=True)
else:
    st.dataframe(alldf, use_container_width=True, hide_index=True)
