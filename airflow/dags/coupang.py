# coupang crawler

# airflow 관련 모듈
from datetime import timedelta
from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.operators.python import PythonOperator

# task 관련 모듈
from src.coupang_crawler import OpenPyXL
import os
import time
import pandas as pd
import requests

import psycopg2.extras
from sqlalchemy import create_engine

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


def coupang_review() -> None:
    # PostgreSQL에서 data 불러오기
    URL = "postgresql+psycopg2://sumin:sumin@101.101.210.35:30005/djangodb"
    engine = create_engine(URL, echo=False)

    pg_query = "select * from coffee_bean_bean where coupang_link is not null and roastery = '콩스콩스'"
    df = pd.read_sql_query(pg_query, con=engine)

    start = time.time()
    for url in df["coupang_link"]:
        # url이 없는 경우 pass
        if url is None:
            continue
        else:  # url이 유효하다면 실행
            try:
                requests.get(url)
            except requests.exceptions.RequestException:
                logger.info(f"유효하지 않은 URL입니다. {df['title']} 리뷰 데이터 수집 실패!")
                continue

        title = df["title"]
        roastery = df["roastery"]
        OpenPyXL.save_file(
            title, roastery, url=url, save_none_contents=True
        )  # 항상 내용이 없어도 수집

    end = time.time()

    logger.info(f"\n{end - start:.4f}초가 소요되었습니다.\n")


def transform_load_review() -> None:
    URL = "postgresql+psycopg2://sumin:sumin@101.101.210.35:30005/djangodb"
    engine = create_engine(URL, echo=False)

    # PostgreSQL 연결
    conn = engine.raw_connection()
    cursor = conn.cursor()

    # raw data를 하나씩 읽어오며 DB에 INSERT 후 삭제
    for file in os.listdir("/opt/ml/coffee/dataset/raw_data/reviews/coupang"):
        reviews = pd.read_csv(file)  # review data
        roastery = reviews["로스터리"].unique()[0]
        # review data와 원두 아이디 매칭하기 위해 DB에서 원두 데이터 불러오기
        pg_query = f"select * from coffee_bean_bean where coupang_link is not null and roastery = '{roastery}'"
        coffee = pd.read_sql_query(pg_query, con=engine)

        # 원두 데이터와 리뷰 데이터 merge
        merged_df = pd.merge(
            coffee[["id", "title", "roastery"]],
            reviews,
            left_on=["title", "roastery"],
            right_on=["원두이름", "로스터리"],
        )
        merged_df = merged_df.drop("title", axis=1)
        merged_df = merged_df.rename(
            columns={
                "id": "bean_id_id",
                "리뷰 제목": "title",
                "구매자 이름": "user_nickname",
                "구매자 평점": "rating",
                "리뷰 내용": "content",
                "맛 만족도": "taste_satisfaction",
            }
        )
        merged_df = merged_df[
            [
                "title",
                "user_nickname",
                "rating",
                "content",
                "taste_satisfaction",
                "bean_id_id",
            ]
        ]

        # DB에 execute_values 를 이용한 INSERT
        # 삽입할 데이터의 칼럼 목록
        columns = merged_df.columns.tolist()

        # 삽입할 데이터의 값들을 튜플 형태로 변환
        values = [tuple(x) for x in merged_df.values]

        # 삽입할 SQL 문
        insert_sql = (
            f"INSERT INTO coffee_bean_beanreview ({', '.join(columns)}) VALUES %s"
        )

        # execute_values()를 사용하여 데이터 삽입
        psycopg2.extras.execute_values(
            cursor, insert_sql, values, template=None, page_size=1000
        )

        logger.info(f"{reviews['원두이름']} 데이터 Load 완료!")

    # 변경사항 커밋
    conn.commit()

    # 연결 종료
    conn.close()


# with 구문으로 DAG 정의를 시작합니다.
with DAG(
    dag_id="coupang_review",  # DAG의 식별자용 아이디
    description="쿠팡 리뷰 배치단위 수집(크롤링)",  # DAG에 대한 설명
    start_date=days_ago(2),  # DAG 정의 기준 2일 전부터 시작
    schedule_interval="0 0 * * *",  # 매일 자정에 실행
    tags=["review_coupang"],  # 태그는 리뷰로 설정
) as dag:
    # 테스크를 정의합니다.

    # python 함수인 coupang_review()를 실행해 raw data를 csv 형태로 반환합니다.
    t1 = PythonOperator(
        task_id="extract_law_data",
        python_callable=coupang_review,
        depends_on_past=True,
        owner="sumin",
        retries=3,
        retry_delay=timedelta(minutes=10),
    )

    # coupang_review()를 통해 수집된 raw data를 전처리 후 DB에 load합니다.
    t2 = PythonOperator(
        task_id="transform_load_data",
        python_callable=transform_load_review,
        depends_on_past=True,
        owner="sumin",
        retries=3,
        retry_delay=timedelta(minutes=5),
    )

    # 테스크 순서를 정합니다.
    # t1 실행 후 t2를 실행합니다.
    t1 >> t2
