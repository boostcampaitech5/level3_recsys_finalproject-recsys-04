import numpy as np
import pandas as pd

import yaml

from typing import List, Optional

from feature_engineering import feature_engineering
from sqlalchemy import create_engine


def load_config(args):
    with open(f"./config/CBF.yaml") as f:
        config = yaml.load(f, Loader=yaml.FullLoader)
        config = config[f"{args.config_name}"]
        print("----- config -----")
        print(config)
        print("--------------------")

    return config


def load_table(query: str) -> pd.DataFrame:
    """
    DB에서 아이템 데이터와 리뷰 데이터를 가져옵니다.

    Parameters
    ----------
    query : str
        SQL query

    Returns
    -------
    pd.DataFrame : 쿼리로 불러온 테이블
    """
    URL = "postgresql+psycopg2://yerim:yerim@101.101.210.35:30005/djangodb"
    engine = create_engine(URL, echo=False)

    table = pd.read_sql_query(query, con=engine)

    return table


def load_item_profile(
    target_item_ids: Optional[List[int]] = None, all: bool = False
) -> pd.DataFrame:
    """
    콘텐츠 기반 필터링에 필요한 데이터를 불러옵니다.

    Parameters
    ----------
    target_item_ids: Optional[List[int]
        - 타겟 아이템 아이디 리스트 (CF의 추천 결과)
        - 해당 값이 있으면 not cole start, 없으면 cold start (user preference로 추천)

    all: bool = False
        - True 이면 타겟 아이템 상관 없이 모든 아이템에 대해 연산

    Returns
    -------
    pd.DataFrame : 전처리가 완료된, 유사도 계산에 쓰일 아이템 프로파일
    """
    # -- 데이터셋 로드
    load_all_items_query = "select * from coffee_bean_bean"
    load_all_reviews_query = "select * from coffee_bean_beanreview"
    items = load_table(load_all_items_query)
    reviews = load_table(load_all_reviews_query)

    # -- 전처리
    items = preprocess(items, reviews, target_item_ids, all=all)

    # -- 피쳐 선택
    features_to_use = [
        "id",
        "aroma",
        "acidity",
        "sweetness",
        "body",
        "roasting_point",
    ]

    if target_item_ids or all:  # 타겟이 아이템인 경우 - 즉 콜드 스타트가 아닌 경우, 키워드 관련 피쳐도 추가
        keywords_jaccard_sim_features = [
            col for col in items.columns if "keywords_jaccard_sim" in col
        ]
        features_to_use += (
            keywords_jaccard_sim_features  # 값의 범위가 이미 0 ~ 1이므로 10으로 나누지 않음
        )

    # -- 아이템 프로파일 구축
    item_profile = build_item_profile(
        items, features_to_use, features_to_use[1:6]
    )

    return item_profile


def preprocess(
    items: pd.DataFrame,
    reviews: pd.DataFrame,
    target_item_ids: Optional[List[int]] = None,
    all: bool = False,
) -> pd.DataFrame:
    """
    콘텐츠 기반 필터링에 사용할 데이터셋(원두 데이터)의 전처리를 진행합니다.

    Parameters
    ----------
    items : pd.DataFrame
        아이템 데이터셋

    reviews : pd.DataFrame
        리뷰 데이터셋

    target_item_ids: Optional[List[int]]
        타겟 아이템의 id 리스트

    all: bool = False
        - True 이면 타겟 아이템 상관 없이 모든 아이템에 대해 연산

    Returns
    -------
    pd.DataFrame : 전처리 된 아이템 데이터셋
    """

    # -- 사용할 필요 없는 컬럼 제거
    items = items.drop(columns=["coupang_link"])

    # -- 피쳐 엔지니어링 - 리뷰 관련 피쳐 추가
    items = feature_engineering(items, reviews, target_item_ids, all=all)

    # -- 결측치 처리
    # 콩스콩스 로스터리에서 리뷰 수가 결측인 경우는 리뷰가 없었기 때문이므로, 해당 경우는 평점과 리뷰 수를 모두 0으로 대체
    mask_idx = items[
        (items["roastery"] == "콩스콩스") & (items["review_count"].isna())
    ].index  # 리뷰가 없는 콩스콩스 상품들의 인덱스
    items.loc[mask_idx, ["review_count", "rating"]] = 0

    # 나머지 리뷰 수 및 평점, 그리고 향미의 결측치들은 모두 중앙값으로 대체
    for feature_name in ["review_count", "rating", "aroma"]:
        items = fill_to_median(items, feature_name)

    return items


def build_item_profile(
    items: pd.DataFrame,
    features_to_use: List[str],
    features_to_scale: List[str],
) -> pd.DataFrame:
    """
    사용할 피쳐만 선택하고 각 피쳐의 값의 범위를 통일하여, 유사도 계산에 쓰일 아이템 행렬을 완성합니다.

    Parameters
    ----------
    items : pd.DataFrame
        전처리 된 아이템 데이터셋

    features_to_use: List[str]
        유사도 계산에 쓸 피쳐 리스트

    features_to_scale: List[str]
        각 피쳐의 값의 범위를 통일하기 위해 스케일링 할 피쳐 리스트

    Returns
    -------
    pd.DataFrame : 유사도 계산에 쓰일 아이템 행렬
    """
    # item_profile = items.set_index("id")[features_to_use].copy()
    item_profile = items[features_to_use].copy()
    item_profile[features_to_scale] = item_profile[features_to_scale] / 10

    return item_profile


def fill_to_median(data: pd.DataFrame, feature_name: str) -> pd.DataFrame:
    """
    데이터셋 내 원하는 피쳐들에 대해 결측치를 중앙값으로 대체합니다.

    Parameters
    ----------
    data : pd.DataFrame
        결측치를 채우고자 하는 데이터셋

    feature_name : str
        결측치를 채우고 싶은 피쳐의 이름

    Returns
    -------
    pd.DataFrame : 결측치가 채워진 데이터셋
    """
    data.loc[data[feature_name].isna(), feature_name] = data[
        feature_name
    ].median()

    return data
