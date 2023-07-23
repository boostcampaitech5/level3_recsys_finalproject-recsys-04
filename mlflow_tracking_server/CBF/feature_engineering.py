import os

import numpy as np
import pandas as pd

from tqdm import tqdm

from keybert import KeyBERT
from kiwipiepy import Kiwi
from transformers import BertModel

from typing import List, Tuple, Set


def feature_engineering(
    items: pd.DataFrame,
    reviews: pd.DataFrame,
    target_item_ids: List[int] = None,
    all: bool = False,
) -> pd.DataFrame:
    """
    아이템 데이터셋에 대해 새로운 피쳐를 만들어 추가합니다.

    Parameters
    ----------
    items : pd.DataFrame
        아이템 데이터셋

    reviews : pd.DataFrame
        리뷰 데이터셋

    target_item_ids : List[int]
        타겟 아이템 아이디 리스트 (CF의 추천 결과)

    all: bool = False
        - True 이면 타겟 아이템 상관 없이 모든 아이템에 대해 연산

    Returns
    -------
    pd.DataFrame : 피쳐가 추가된 데이터셋
    """

    # -- review 데이터로부터 관련 피쳐 생성
    review_features = (
        (reviews.groupby("bean_id_id")["rating"].count())
        .to_frame()
        .reset_index()
        .rename(columns={"rating": "review_count"})
    )

    items = items.merge(
        review_features, how="left", left_on="id", right_on="bean_id_id"
    )

    # -- item description으로부터 키워드 추출 - 키워드 피쳐 생성
    items = extract_keywords(items)

    # -- 추출한 키워드 피쳐로부터 자카드 유사도를 계산한 피쳐 생성
    if not os.path.exists(
        "/opt/ml/Recommendation-Modeling/mlflow_tracking_server/CBF/item-item_cosine_sim.pkl"
    ):
        if target_item_ids:  # 타겟이 아이템인 경우 - 즉 콜드 스타트가 아닌 경우
            for target_item_id in target_item_ids:
                items = make_keyword_feature(items, target_item_id)

        elif all:
            for item_id in items["id"]:
                items = make_keyword_feature(items, item_id)
    else:
        pass

    return items


def make_keyword_feature(
    items: pd.DataFrame, target_item_id: int
) -> pd.DataFrame:
    """
    아이템 데이터셋에 대해 키워드 관련 피쳐를 추가합니다.

    Parameters
    ----------
    items : pd.DataFrame
        아이템 데이터셋

    target_item_id : int
        타겟 아이템의 아이디

    Returns
    -------
    pd.DataFrame : 키워드 관련 피쳐가 추가된 아이템 데이터셋
    """

    # 타겟 아이템과 이외 아이템들의 키워드 간 자카드 유사도를 계산해 피쳐 생성
    target = items[items["id"] == target_item_id]  # 타겟 아이템 지정

    # 타겟 아이템에 대한 키워드 자카드 유사도 계산
    new_items = items.copy()
    col_name = f"{target_item_id}_keyword_jaccard_sim"
    new_items[col_name] = items.apply(
        lambda row: jaccard_similarity(
            target["keywords_set"].values[0], row["keywords_set"]
        ),
        axis=1,
    )

    return new_items


def nouns_extractor(text: str, kiwi) -> str:
    """
    입력 받은 텍스트로부터 명사를 추출합니다.

    Parameters
    ----------
    text : str
        명사를 추출할 대상이 되는 텍스트

    kiwi : 한국어 형태소 분석기 인스턴스

    Returns
    -------
    str : 입력 받은 텍스트로부터 명사만 추출해 남긴 텍스트

    Examples
    --------
    >>> nouns_extractor("이것은 예시입니다.")
    이것 예시
    """
    nouns_list = []
    result = kiwi.analyze(text)
    for token, pos, _, _ in result[0][0]:
        if len(token) != 1 and pos.startswith("N") or pos.startswith("SL"):
            nouns_list.append(token)

    nouns_text = " ".join(nouns_list)

    return nouns_text


def extract_keywords(items: pd.DataFrame) -> pd.DataFrame:
    """
    키워드를 추출하여 피쳐를 추가합니다.

    Parameters
    ----------
    data: pd.DataFrame
        키워드 피쳐를 추가하고자 하는 데이터셋

    Returns
    -------
    pd.DataFrame : 키워드 피쳐가 추가된 데이터셋
    """
    kiwi = Kiwi()

    # -- 명사 추출
    sentences_list = [
        nouns_extractor(text, kiwi)
        for text in tqdm(items["description"], desc="Extracting nouns")
    ]

    # -- 키워드 추출
    model = BertModel.from_pretrained("skt/kobert-base-v1")
    kw_model = KeyBERT(model)

    keywords_list = []
    for sentence in tqdm(sentences_list, desc="Extracting keywords"):
        keywords = kw_model.extract_keywords(  # (키워드, 확률) 형식의 결과 반환
            sentence, keyphrase_ngram_range=(1, 1), stop_words=None, top_n=20
        )
        keywords_list.append(keywords)

    # -- 키워드 피쳐 추가
    items = add_keywords_features(items, keywords_list)

    return items


def select_unnecessary_keywords(keywords_list: List[str]) -> List[str]:
    """
    필요 없는 키워드를 선정합니다.

    Parameters
    ----------
    keywords_list : List[List[Tuple[str, float]]]
        키워드를 담고 있는 리스트

    Returns
    -------
    List[str] : 입력 받은 키워드들 중, 필요 없는 키워드를 골라 담은 리스트

    """
    all_keywords_list = []
    for keywords in keywords_list:
        res = [keyword for keyword, _ in keywords]
        all_keywords_list.extend(res)

    all_keywords_cnt = pd.Series(all_keywords_list).value_counts()

    unnecessary_keywords = [
        "커피",
        "특징",
        "원두",
        "기분",
        "느낌",
        "추천",
        "누구",
        "표현",
        "약간",
        "이름",
        "사용",
        "제거",
        "배전",
        "적합",
        "지역",
        "유지",
        "사이",
        "초점",
        "가지",
        "상품",
        "각종",
        "추출",
        "모금",
        "우리",
        "정도",
        "세팅",
        "최대한",
    ]

    eng_digit_keywords_list = [
        keyword
        for keyword in all_keywords_cnt.index
        if any(ord(char) < 128 or char.isdigit() for char in keyword)
    ]

    # 불필요한 키워드 리스트
    remove_keywords_list = list(
        set(
            all_keywords_cnt[
                all_keywords_cnt <= 2
            ].index.tolist()  # 2번 이하 등장한 키워드
            + unnecessary_keywords  # 직접 선정한 불필요한 키워드
            + eng_digit_keywords_list  # 영어나 숫자를 포함한 키워드
        )
    )

    return remove_keywords_list


def add_keywords_features(
    items: pd.DataFrame, keywords_list: List[List[Tuple[str, float]]]
) -> pd.DataFrame:
    """
    추출한 키워드를 활용하여 만든 feature를 데이터셋에 추가합니다.

    Parameters
    ----------
    data : pd.DataFrame
        키워드 관련 피쳐를 추가할 아이템 데이터셋

    keywords_list : List[List[Tuple[str, float]]]
        키워드를 담고 있는 리스트

    Returns
    -------
    pd.DataFrame : 키워드 관련 피쳐를 담은 데이터셋

    """
    description_keywords_list = []
    description_keywords_sentence = []
    unnecessary_keywords_list = select_unnecessary_keywords(keywords_list)

    for keywords in keywords_list:
        # 키워드를 집합으로 저장
        keywords_set = {
            keyword
            for keyword, _ in keywords
            if keyword not in unnecessary_keywords_list
        }
        description_keywords_list.append(keywords_set)

        # 키워드만 뽑아 공백으로 구분하여 하나의 문자열로 합치기
        keywords_sentence = " ".join(
            [
                keyword
                for keyword, _ in keywords
                if keyword not in unnecessary_keywords_list
            ]
        )
        description_keywords_sentence.append(keywords_sentence)

    items["keywords_set"] = description_keywords_list
    items["keywords_sentence"] = description_keywords_sentence

    return items


def jaccard_similarity(set1: Set[str], set2: Set[str]) -> float:
    """
    입력 받은 두 집합에 대해 자카드 유사도를 계산합니다.

    Parameters
    ----------
    set1 : Set[str]
        자카드 유사도를 계산할 첫 번째 집합

    set2 : Set[str]
        자카드 유사도를 계산할 두 번째 집합

    Returns
    -------
    float : 두 집합에 대한 자카드 유사도 값
    """
    intersection = len(set1.intersection(set2))
    union = len(set1.union(set2))

    if union == 0:
        return 0  # 분모가 0인 경우 자카드 유사도를 0으로 반환

    similarity = intersection / union
    return similarity
