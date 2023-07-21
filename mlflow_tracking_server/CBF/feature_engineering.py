import numpy as np
import pandas as pd

import os
from tqdm import tqdm

from keybert import KeyBERT
from kiwipiepy import Kiwi
from transformers import BertModel

from typing import List, Set


def feature_engineering(
    item_data: pd.DataFrame, merged_data: pd.DataFrame, config
):
    """
    아이템 데이터셋에 대해 새로운 피쳐를 만들어 추가합니다.

    Parameters
    ----------
    item_data : pd.DataFrame
        아이템 정보를 담고 있는 데이터셋

    merged_data : pd.DataFrame
        아이템과 리뷰 정보를 담고 있는 통합 데이터셋

    config : 타겟 아이템 이름을 포함한 설정 정보

    Returns
    -------
    pd.DataFrame : 피쳐가 추가된 데이터셋
    """

    ### 1. 통합 데이터의 리뷰 관련 데이터로부터 피쳐 생성
    review_features = (
        merged_data.groupby("상품명")["구매자 평점"]
        .agg(["mean", "count"])
        .reset_index()
        .rename(columns={"mean": "평점", "count": "리뷰 수"})
    )
    review_features["평점"] = review_features["평점"].round(2)
    review_features["리뷰 수"] = review_features["리뷰 수"].astype(int)

    data = item_data.merge(review_features, how="left")

    # if config["target_item_name"]:
    #     make_keyword_feature(data, config)

    return data


def make_keyword_feature(data, config):
    ### 키워드 추출 - 키워드 피쳐 생성
    data = extract_keywords(data)

    ### 타겟 아이템과 이외 아이템들의 키워드 간 자카드 유사도를 계산해 피쳐 생성
    target = data[data["상품명"] == config["target_item_name"]]  # 타겟 아이템 지정

    # 타겟 아이템에 대한 키워드 자카드 유사도 계산
    keywords_jaccard_similarity_df = data.apply(
        lambda row: jaccard_similarity(
            target["keywords_set"].values[0], row["keywords_set"]
        ),
        axis=1,
    ).to_frame(name="keyword_jaccard_similarity")

    # 피쳐 저장
    save_path = os.path.join(
        config["result_path"],
        config["target_item_name"],
    )
    if not os.path.exists(save_path):
        os.makedirs(save_path, exist_ok=True)

    keywords_jaccard_similarity_df.to_csv(
        os.path.join(save_path, "keyword_jaccard_similarity.csv"),
        index=False,
    )

    return keywords_jaccard_similarity_df


def nouns_extractor(text: str, kiwi) -> str:
    """
    입력 받은 텍스트로부터 명사를 추출합니다.

    Parameters
    ----------
    text : str
        명사를 추출할 대상이 되는 텍스트

    Returns
    -------
    str : 입력 받은 텍스트로부터 명사만 추출해 남긴 텍스트

    Examples
    --------
    >>> nouns_extractor("이것은 예시입니다.")
    이것 예시
    """

    # kiwi = Kiwi()

    nouns_list = []
    result = kiwi.analyze(text)
    for token, pos, _, _ in result[0][0]:
        if len(token) != 1 and pos.startswith("N") or pos.startswith("SL"):
            nouns_list.append(token)

    nouns_text = " ".join(nouns_list)

    return nouns_text


def extract_keywords(data: pd.DataFrame) -> pd.DataFrame:
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

    # 명사 추출
    sentences_list = [
        nouns_extractor(text, kiwi)
        for text in tqdm(data["text"], desc="Extracting nouns")
    ]

    # 키워드 추출
    model = BertModel.from_pretrained("skt/kobert-base-v1")
    kw_model = KeyBERT(model)

    keywords_list = []
    for sentence in tqdm(sentences_list, desc="Extracting keywords"):
        keywords = kw_model.extract_keywords(  # (키워드, 확률) 형식의 결과 반환
            sentence, keyphrase_ngram_range=(1, 1), stop_words=None, top_n=20
        )
        keywords_list.append(keywords)

    # 키워드 피쳐 추가
    data = add_keywords_features(data, keywords_list)

    return data


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
    data: pd.DataFrame, keywords_list: List
) -> pd.DataFrame:
    """
    추출한 키워드를 활용하여 만든 feature를 데이터셋에 추가합니다.

    Parameters
    ----------
    data : pd.DataFrame
        키워드 관련 피쳐를 추가할 데이터셋

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

    data["keywords_set"] = description_keywords_list
    data["keywords_sentence"] = description_keywords_sentence

    return data


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
