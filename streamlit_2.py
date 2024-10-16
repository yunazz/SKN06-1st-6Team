# app.py
import streamlit as st
import pandas as pd
import json

padding = 0
st.set_page_config(page_title="전기차 보조금", layout="wide", page_icon="📍")

## json 파일 읽어오는 함수
def read_json(path):
    df = pd.read_json(path)
    return df

## 파일 전처리
cardf = read_json("../car.json") # server/crawling/data/car.json
citydf = read_json("../city.json") # server/crawling/data/city.json
# dtaildf = read_json("car_detail.json") # server/crawling/data/car_detail.json
with open("../car_detail.json", 'rt', encoding='utf-8') as fo:
    dtail = json.loads(fo.read())

## SelectBox 함수
def get_list(condition, name):
    # 값 연동이 필요하면 condition에서 select된 값, 그렇지 않다면 None
    # 예시) get_list(state, 'city_name')
    if name == 'city_name':
        selected = cardf[(cardf['state'] == condition)][name]
    elif name == 'car_name':
        selected = cardf[(cardf['maker'] == condition)][name]
    else:
        selected = cardf[name]
    result1 = dict.fromkeys(selected)
    result2 = list(result1)
    return result2


## Sidebar
with st.sidebar:
    state = st.selectbox('시/도를 고르세요', get_list(None, 'state'))    # state
    city = st.selectbox('지역을 고르세요', get_list(state,'city_name'))  # city
    maker = st.selectbox('판매사를 고르세요',get_list(None, 'maker'))    # brand
    car = st.selectbox('모델을 고르세요',get_list(maker, 'car_name'))    # model

    pressed = st.button("조회")


## 값 받아오기
# 선택된 차량의 정보
for info in dtail:
    if info['차종'] == car:
        detail = info
# 선택된 지역의 지원금 정보
sub = cardf[(cardf['city_name'] == city) & (cardf['car_name'] == car)]
sub.drop(['state', 'city_name'], axis = 1, inplace = True)
sub['total_subsidy'] = sub['national_subsidy'] + int(sub['city_subsidy'])
sub.columns = ['차종', '판매사', '모델명', '국고보조금', '지자체보조금', '총 지원금']
# 선택된 지역의 지자체 연락처 정보
phone = citydf[citydf['city_name'] == city]
# 선택된 지역 외 지원금 정보
total = cardf[cardf['car_name'] == car]
total.drop(['maker', 'car_name'], axis = 1, inplace = True)
total.columns = ['차종', '국고보조금', '지자체보조금', '시/도', '지역구분']


## 화면 구성
# 수정 필요 진짜 임의적으로 만든 것
if pressed:
    st.subheader(f"{city}에서 받을 수 있는 {car}의 지원금입니다.")
    st.dataframe(sub, hide_index=True)
    col1, col2 = st.columns(2)
    with col1:
        if pressed:
            st.subheader(f"{car} 정보")
            st.write(detail)
    with col2:
        if pressed:
            st.subheader(f"{city}의 관할 부서 연락처")
            st.dataframe(phone, hide_index=True)
    st.subheader(f"{city}를 포함한 다른 지역의 {car} 지원금")
    st.dataframe(total, hide_index=True)
else:
    st.write("초기화면초기화면")
