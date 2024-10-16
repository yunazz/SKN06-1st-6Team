## SQL이 있는 경우
import streamlit as st
import pandas as pd
import pymysql
from sqlalchemy import create_engine
# from app import password
###################################
import json
###################################

with st.popover("password"):
    password = st.text_input("root 비밀번호를 입력해주세요")


## DB 연결 설정
def do_con(password):
    db_connection_str = f'mysql+pymysql://root:{password}@localhost/SKN06_6Team'
    db_connection = create_engine(db_connection_str)
    return db_connection

db_connection = do_con(password)

## SQL 실행 함수
def read_df(query):
    df = pd.read_sql_query(query, db_connection)
    return df


## SelectBox 함수
# 데이터베이스에서 시도 목록 가져오기
def get_state_names():
    query = 'SELECT DISTINCT state FROM city'
    df = pd.read_sql_query(query, db_connection)
    return df

# 데이터베이스에서 지역구분 목록 가져오기
def get_city_names(state):
    query = f'SELECT DISTINCT city_name FROM city WHERE state = "{state}"'
    df = pd.read_sql_query(query, db_connection)
    return df

# 데이터베이스에서 차량 제조사 목록 가져오기
def get_maker_names():
    query = 'SELECT DISTINCT maker FROM car'
    df = pd.read_sql_query(query, db_connection)
    return df

# 데이터베이스에서 차량 모델 목록 가져오기
def get_model_names(maker):
    query = f'SELECT DISTINCT car_name FROM car WHERE maker = "{maker}"'
    df = pd.read_sql_query(query, db_connection)
    return df

####################################################################
# car_detail 가져오기(DB에 추가 필요)
with open("server/crawling/data/car_detail.json", 'rt', encoding='utf-8') as fo:
    dtail = json.loads(fo.read())
####################################################################

## Sidebar
# sidebar에 셀렉박스 배치
with st.sidebar:
    state_names = get_state_names()
    state = st.selectbox('시/도를 고르세요',state_names)  # state

    city_names = get_city_names(state)
    city = st.selectbox('지역을 고르세요',city_names)  # city

    maker_names = get_maker_names()
    maker = st.selectbox('판매사를 고르세요',maker_names) # brand

    car_names = get_model_names(maker)
    car = st.selectbox('모델을 고르세요',car_names) # model

    pressed = st.button("조회")


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

# car_detail
###############################################
# 선택된 차량의 정보
for info in dtail:
    if info['car_name'] == car:
        detail = info
###############################################

## 데이터 불러오기
sub = read_df(q1)
phone = read_df(q2)
total = read_df(q3)

## 화면 구성
if pressed:
    st.dataframe(sub, hide_index=True)
    col1, col2 = st.columns(2)
    with col1:
        st.write(detail)
    with col2:
        st.dataframe(phone, hide_index=True)
    st.dataframe(total, hide_index=True)
    end = st.button("종료")
    if end:
        del password
        engine.dispose()
else:
    st.write("SQL을 사용하여 데이터를 불러오는 페이지입니다.")
