import streamlit as st
import pandas as pd
import pymysql
from sqlalchemy import create_engine
import json


## 전반적인 화면 설정
padding = 0
st.set_page_config(page_title="전기차 보조금", layout="wide", page_icon="📍")

with st.form("init"):
    install = st.radio("MySQL에 데이터를 설치할까요? root 비밀번호만 알려주시면 됩니다.", ["예", "아니오"], captions=["SQL에서 새로 DB와 Table을 만든 후 불러옵니다.", "Repositary에 있는 json 파일로 불러옵니다."])
    submit = st.form_submit_button("확인")
if submit:
    if install == "예":
        st.page_link("pages/use_sql.py", label = "클릭")
    else:
        st.page_link("pages/use_json.py", label = "클릭")
