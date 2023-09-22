# naver crawler

# airflow 관련 모듈
from datetime import timedelta
from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.operators.python import PythonOperator

# task 관련 모듈
import os
import time
import pandas as pd

import psycopg2.extras
from sqlalchemy import create_engine

# crawler 관련 모듈
from src.naver.utils import OpenPyXL
from src.naver.utils import get_driver
from src.naver.crawling_strategy import get_review_in_page

# log 관련 모듈
import logging

# 로거 인스턴스 생성
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# 콘솔 핸들러 생성
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

# 로그 포맷 설정
log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
formatter = logging.Formatter(log_format)
console_handler.setFormatter(formatter)

# 콘솔 핸들러를 로거에 추가
logger.addHandler(console_handler)


def naver_review() -> None:
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"  # 사용자에 맞게 수정 : 구글에 user agent 검색
    url = "https://smartstore.naver.com/blackbeans/products/310288062"

    driver = get_driver(user_agent=user_agent)
    driver.get(url)
    time.sleep(5)

    if not os.path.exists("/opt/ml/coffee/dataset/raw_data/reviews/naver"):
        os.mkdir("/opt/ml/coffee/dataset/raw_data/reviews/naver")

    save_data = get_review_in_page(driver)
    OpenPyXL.save_file(save_data)


def transform_review() -> None:
    URL = "postgresql+psycopg2://sumin:sumin@101.101.210.35:30005/djangodb"
    engine = create_engine(URL, echo=False)

    roastery = "콩스콩스"  # 이후에 다른 스토어도 추가될 수 있게 변경돼야 됨
    # review data와 원두 아이디 매칭하기 위해 DB에서 원두 데이터 불러오기
    pg_query = f"select * from coffee_bean_bean where roastery = '{roastery}'"
    coffee = pd.read_sql_query(pg_query, con=engine)

    file_path = "/opt/ml/coffee/dataset/raw_data/reviews/naver/"
    files = [i for i in os.listdir(file_path) if i[-3:] == "csv"]  # t1으로 저장된 raw_data

    results = pd.DataFrame(
        columns=[
            "title",
            "user_nickname",
            "rating",
            "content",
            "taste_satisfaction",
            "bean_id_id",
            "date",
            "platform",
        ]
    )

    for file in files:
        raw_data = pd.read_csv(file_path + file)
        os.remove(file_path + file)
        print(f"원본 데이터: {raw_data.shape}")

        # 고쳐야 할 샘플들의 인덱스
        wrong_idx = raw_data[raw_data["상품명"].apply(lambda row: "샵N" in row)].index

        # 상품명 컬럼에 담긴 grind 정보 추출
        right_grind = (
            raw_data.loc[wrong_idx, "상품명"]
            .apply(lambda row: row.split("샵N ")[1])
            .rename("grind")
        )

        # grind 컬럼에 담긴 weight, 상품명 정보 추출
        split_grind = raw_data.loc[wrong_idx, "grind"].apply(lambda row: row.split("_"))
        right_weight = split_grind.apply(lambda split_list: split_list[0]).rename(
            "weight"
        )
        right_name = split_grind.apply(lambda split_list: split_list[-1]).rename("상품명")

        right_weight = right_weight.apply(
            lambda row: "1000g" if row == "kg" else "500g"
        )

        # 올바른 정보
        right_info = pd.concat([right_name, right_grind, right_weight], axis=1)

        # 기존 잘못된 정보들을 올바른 정보로 변경
        data = raw_data.copy()
        data.loc[wrong_idx, ["상품명", "grind", "weight"]] = right_info

        data = data.drop(["grind", "weight"], axis=1)

        # 상품명 전처리
        # 1. (NEW) 지워주기
        data["상품명"] = data["상품명"].apply(lambda x: x.replace("(NEW)", "").strip())

        # 2. 원두 이름 통일 시켜주기
        transform_bean_name = {
            "베트남 로부스타 블루드래곤 워시드G1": "베트남 블루드래곤 로부스타 워시드 G1",
            "브라질 세하도 ny-2 17-18": "브라질 세하도 NY-2 17-18",
            "디카페인 브라질 산토스": "디카페인 브라질",
            "에티오피아 예가체프 G2 워시드": "에티오피아 예가체프 G2",
            "디카페인 과테말라 SHB": "디카페인 과테말라",
            "멕시코 알투라 SHG": "멕시코 알투라 SHG 워시드",
            "엘살바도르팬시 SHG": "엘살바도르 팬시 SHG 워시드",
            "베트남 로부스타 블루드래곤 G1": "베트남 블루드래곤 로부스타 워시드 G1",
        }

        # "상품명" 컬럼에 딕셔너리를 적용하여 값 변환
        data["상품명"] = data["상품명"].replace(transform_bean_name)
        # 품절 상품 drop
        data = data[~data["상품명"].isin(["티파니 블렌드", "인도 몬순 말라바AA"])]

        # column명 변경
        modify_columns = {
            "구매자 이름": "user_nickname",
            "구매자 평점": "rating",
            "리뷰 내용": "content",
            "맛 만족도": "taste_satisfaction",
        }

        data = data.rename(columns=modify_columns)

        # date 전처리
        # ex) '23.07.18.' 형태의 문자열을 datetime 객체로 변환
        data["date"] = pd.to_datetime(data["date"], format="%y.%m.%d.")

        # datetime 객체를 PostgreSQL의 timestamp with time zone 형식으로 변환
        data["date"] = data["date"].dt.strftime("%Y-%m-%d %H:%M:%S")

        # 플랫폼
        data["platform"] = "네이버"
        data["로스터리"] = roastery

        # 원두 정보랑 리뷰 정보 합치기
        merged_df = pd.merge(
            coffee[["id", "title", "roastery"]],
            data,
            left_on=["title", "roastery"],
            right_on=["상품명", "로스터리"],
        )
        merged_df = merged_df.drop("title", axis=1)
        merged_df = merged_df.rename(columns={"id": "bean_id_id", "상품명": "title"})
        merged_df = merged_df[
            [
                "title",
                "user_nickname",
                "rating",
                "content",
                "taste_satisfaction",
                "bean_id_id",
                "date",
                "platform",
            ]
        ]

        print(
            f"원본 데이터 상품개수: {data['상품명'].nunique()}, 전처리 데이터 상품개수: {merged_df['title'].nunique()}"
        )
        print(f"전처리된 데이터의 총 rows: {merged_df.shape[0]}")

        results = pd.concat([results, merged_df], ignore_index=True)

    results = results.drop_duplicates()  # 중복 데이터 제거
    results.to_csv(
        "/opt/ml/coffee/dataset/preprocessed/naver/naver_results.csv", index=False
    )


def load_review() -> None:
    result_file = "/opt/ml/coffee/dataset/preprocessed/naver/naver_results.csv"
    results = pd.read_csv(result_file)  # 전처리된 데이터

    # DB에 execute_values 를 이용한 INSERT
    # 삽입할 데이터의 칼럼 목록
    columns = results.columns.tolist()

    # 삽입할 데이터의 값들을 튜플 형태로 변환
    values = [tuple(x) for x in results.values]

    # 삽입할 SQL 문
    insert_sql = f"INSERT INTO coffee_bean_beanreview ({', '.join(columns)}) VALUES %s"

    # PostgreSQL 연결
    URL = "postgresql+psycopg2://sumin:sumin@101.101.210.35:30005/djangodb"
    engine = create_engine(URL, echo=False)

    conn = engine.raw_connection()
    cursor = conn.cursor()

    # execute_values()를 사용하여 데이터 삽입
    psycopg2.extras.execute_values(
        cursor, insert_sql, values, template=None, page_size=1000
    )

    # 변경사항 커밋
    conn.commit()

    # 연결 종료
    conn.close()


# with 구문으로 DAG 정의
with DAG(
    dag_id="naver_review",  # DAG의 식별자용 아이디
    description="네이버 리뷰 배치단위 수집(크롤링)",  # DAG에 대한 설명
    start_date=days_ago(1),  # DAG 정의 기준 1일 전부터 시작
    schedule_interval="0 0 * * *",  # 매일 06:00에 실행
    tags=["review_naver"],
) as dag:
    # 테스크 정의
    # python 함수인 naver_review()를 실행해 raw data를 csv 형태로 반환
    t1 = PythonOperator(
        task_id="extract_raw_data",
        python_callable=naver_review,
        depends_on_past=True,
        owner="sumin",
        retries=3,
        retry_delay=timedelta(minutes=5),
    )

    # naver_review()를 통해 수집된 raw data를 전처리
    t2 = PythonOperator(
        task_id="transform_data",
        python_callable=transform_review,
        depends_on_past=True,
        owner="sumin",
        retries=3,
        retry_delay=timedelta(minutes=5),
    )

    # 전처리한 데이터를 DB에 load
    t3 = PythonOperator(
        task_id="load_data",
        python_callable=load_review,
        depends_on_past=True,
        owner="sumin",
        retries=3,
        retry_delay=timedelta(minutes=5),
    )

    # 테스크 순서 정의
    # t1 실행 후 t2를 실행
    t1 >> t2 >> t3
