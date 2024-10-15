# SKN01-1st-5Team
<div align="center">
<img width="600" alt="image" src="https://github.com/Jh-jaehyuk/Jh-jaehyuk.github.io/assets/126551524/7ea63fc3-95f0-44d5-a0f0-cf431cae34f1">

[![Hits](https://hits.seeyoufarm.com/api/count/incr/badge.svg?url=https://github.com/SKNETWORKS-FAMILY-AICAMP/SKN01-1st-5Team&count_bg=%2379C83D&title_bg=%23555555&icon=&icon_color=%23E7E7E7&title=hits&edge_flat=false)](https://hits.seeyoufarm.com)

</div>

# 전기차 보조금 조회 어플리케이션 
> **SK Networks AI CAMP 6기** <br/> **개발기간: 2024.10.11 ~ 2024.10.15** 

## 개발팀 소개

| 박유나 | 박미현 | 정유진 | 정민준 |
|:----------:|:----------:|:----------:|:----------:|
| <img width="120px" src="https://github.com/Jh-jaehyuk/Jh-jaehyuk.github.io/assets/126551524/33ea2a85-1853-484b-b2a4-c750f854a26b" /> | <img width="120px" src="https://github.com/Jh-jaehyuk/Jh-jaehyuk.github.io/assets/126551524/b24cae67-75d6-48aa-a94e-e847a769f2c0" /> | <img width="120px" src="https://github.com/Jh-jaehyuk/Jh-jaehyuk.github.io/assets/126551524/a3b96d0b-7537-4670-afaa-57279dab5552" /> |  <img width="120px" src="https://github.com/Jh-jaehyuk/Jh-jaehyuk.github.io/assets/126551524/036ed196-ea34-45d8-bc47-58d84c9927c9" /> |
| [@Yuna Park](https://github.com/yunazz) | [@Park, Mihyeon](https://github.com/ppim321) | [@RealOil](https://github.com/RealOil) | [@MinJun Jung](https://github.com/samking1234-Apple) |

## 프로젝트 개요 및 소개
최근 우리나라는 자동차 업계에 전기자동자 분야가 급 부상하면서 소비자들의 구매욕구가 증가중이다. 그러나, 증가하는 수요와 다르게 보조금 지원 조회가 복잡하고 차량정보 또한 한번에 찾을 수 있는 프로그램은 없었다.
저희는 이러한 불편함을 개선하고자 국내 존재하는 차량 브랜드들의 전기차 정보와 지역별 보조금 정보를 한번에 확인할 수 있는 **통합 검색 어플리케이션**을 구축하였습니다.

## 시작 가이드
### Requirements
For building and running the application you need:

- [MySQL 8.0.37](https://dev.mysql.com/downloads/installer/)
- [Python >= 3.11.7](https://www.python.org/downloads/release/python-3119/)

### Installation
``` bash
$ git clone https://github.com/SKNETWORKS-FAMILY-AICAMP/SKN01-1st-5Team.git
$ cd SKN01-1st-5Team/source
$ pip install -r requirements.txt
```

### Step-by-Step guide
1. `crawling_runner.py` 를 실행하여 브랜드 FAQ를 크롤링합니다.
```bash
$ python3 crawling_runner.py
```

2. `csv_to_db_runner.py` 를 실행하여 크롤링한 데이터를 데이터베이스에 저장합니다.
```bash
$ python3 csv_to_db_runner.py
```

3. **Streamlit**을 이용하여 `runner.py` 웹앱을 작동시킵니다.
```bash
$ streamlit run runner.py
```
---
## Stacks :books:

### Environment
![Visual Studio Code](https://img.shields.io/badge/Visual%20Studio%20Code-007ACC?style=for-the-badge&logo=Visual%20Studio%20Code&logoColor=white)
![Git](https://img.shields.io/badge/Git-F05032?style=for-the-badge&logo=Git&logoColor=white)
![Github](https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=GitHub&logoColor=white)             

### Development
![Python](https://img.shields.io/badge/python-3776AB?style=for-the-badge&logo=python&logoColor=white) 
![MySQL](https://img.shields.io/badge/mysql-4479A1?style=for-the-badge&logo=mysql&logoColor=white)
![Streamlit](https://img.shields.io/badge/streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)

### Communication
![Discord](https://img.shields.io/badge/discord-5865F2?style=for-the-badge&logo=discord&logoColor=white)

## 화면 구성 📺
| ABOUT | FAQ |
| :------------: | :------------: |
| <img width="240px" src="https://github.com/Jh-jaehyuk/Jh-jaehyuk.github.io/assets/126551524/ddffa783-bca1-4ff9-a9d7-d0a2bc65bd6c" />  | <img width="240px" src="https://github.com/Jh-jaehyuk/Jh-jaehyuk.github.io/assets/126551524/141cb773-ffdf-458d-8d52-cc922538117e" /> |

---
## 기능 소개 📦

### 연도별 전국 차량 등록 현황 변화
 - 선택한 지역의 연도별 차량 등록 현황을 그래프로 확인할 수 있습니다.
### 통합 FAQ 검색 시스템
 - 국내 점유율 상위 3개 브랜드 FAQ를 통합 검색할 수 있는 기능을 제공합니다.

---
## 아키텍처

### 디렉토리 구조
```bash
.
├── crawlingDB
│   └── helpers
│       ├── base
│       │   └── crawling_sele.py : Selenium 기반 크롤링 툴 정리
│       ├── connectTB.py : SQL Alchemy를 이용한 DB 연동
│       ├── crawling_genesis.py
│       ├── crawling_hyundai.py
│       ├── crawling_kia.py
│       └── make_brandTB.py : default TABLE 구조 저장
├── crawling_runner.py : 각 브랜드의 FAQ 크롤링
├── csv_to_db_runner.py : csv파일을 이용하여 DB에 데이터 넣기
├── getQuery.py : SQL Alchemy를 이용해 SELECT 쿼리 실행
├── result
│   ├── total_genesis.csv
│   ├── total_hyundai.csv
│   └── total_kia.csv
├── runner.py : Streamlit을 이용한 Webapp runner
└── source
    ├── car.jpg
    ├── home.py
    ├── make_csv.py
    ├── multiapp.py
    ├── page1.py
    ├── page2.py
    └── requirements.txt
```

