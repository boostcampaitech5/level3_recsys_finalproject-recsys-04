import numpy as np
import pandas as pd

import os
import yaml

from typing import Tuple

from sklearn.preprocessing import MinMaxScaler

from feature_engineering import feature_engineering, make_keyword_feature


def load_config(args):
    with open(f"./config/CBF.yaml") as f:
        config = yaml.load(f, Loader=yaml.FullLoader)
        config = config[f"{args.config_name}"]
        print("----- config -----")
        print(config)
        print("--------------------")

    return config


def validate_config(config):
    # config["target_item_name"]과 config["target_user_name"] 둘 중 하나에만 값이 있어야 유효
    if bool(config["target_item_name"]) == bool(config["target_user_name"]):
        print("유저와 아이템 중 하나에 타겟을 설정하세요.")
        return False

    return True


def load_data(config) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    콘텐츠 기반 필터링에 필요한 데이터를 불러옵니다.

    Parameters
    ----------
    config : 데이터 파일 경로를 포함한 설정 정보

    Returns
    -------
    Tuple[pd.DataFrame, pd.DataFrame] : 전처리가 완료된 데이터셋과, 유사도 계산에 쓰일 아이템 행렬
    """

    # 전처리 된 데이터셋 경로
    preprocessed_data = os.path.join(
        config["data_path"],
        "preprocessed_data.csv",
    )

    merged_data = pd.read_csv(config["merged_data_path"])

    if os.path.exists(preprocessed_data):  # 전처리 된 데이터셋이 존재하면 해당 데이터셋을 로드
        data = pd.read_csv(preprocessed_data)
    else:  # 그렇지 않으면 아이템 데이터와 통합 데이터를 불러와 전처리 진행
        item_data = pd.read_csv(config["item_data_path"])
        data = preprocess(item_data, merged_data, config)

    features_to_use = [
        "Cupping Note 향미",
        "Cupping Note 산미",
        "Cupping Note 단맛",
        "Cupping Note 바디감",
        "Roasting Point",
        # "리뷰 수",
    ]

    # 아이템 프로파일
    item_profile = build_item_profile(data, features_to_use, config)

    # 유저 프로파일
    user_profile = build_user_profile(
        merged_data, data, features_to_use, config
    )

    if config["target_item_name"]:  # 타겟 아이템이 있으면
        # 키워드 관련 피쳐 추가
        keyword_feature_path = os.path.join(
            config["result_path"],
            config["target_item_name"],
            "keywords_jaccard_similarity.csv",
        )
        if os.path.exists(keyword_feature_path):
            item_profile["keywords_jaccard_similarity"] = pd.read_csv(
                keyword_feature_path
            )
        else:
            item_profile["keywords_jaccard_similarity"] = make_keyword_feature(
                data, config
            )

    return data, item_profile, user_profile


def preprocess(
    item_data: pd.DataFrame, merged_data: pd.DataFrame, config
) -> pd.DataFrame:
    """
    콘텐츠 기반 필터링에 사용할 데이터셋(원두 데이터)의 전처리를 진행합니다.

    Parameters
    ----------
    item_data : pd.DataFrame
        아이템 정보를 담고 있는 데이터셋

    merged_data : pd.DataFrame
        아이템과 리뷰 정보를 담고 있는 통합 데이터셋

    config : 전처리 된 데이터셋의 저장 경로를 포함한 설정 정보

    Returns
    -------
    pd.DataFrame : 전처리 된 데이터셋
    """

    ### 1. 사용할 필요 없는 컬럼 제거
    item_data = item_data.drop(columns=["validation", "coupang link"])

    ### 1.5. 피쳐 엔지니어링 과정에서의 병합을 위한 전처리 - DB 연결 후 변경 or 제거
    # 통합 데이터의 컬럼명과 통일
    item_data = item_data.rename(columns={"Bean name": "상품명"})

    # 리뷰가 있는 콩스콩스 원두 데이터에 대해 병합을 위해 상품명 통일
    mask = item_data["로스터리"] == "콩스콩스"
    item_data.loc[mask, "상품명"] = change_bean_name(item_data.loc[mask, "상품명"])

    ### 2. 피쳐 엔지니어링 - 리뷰 관련 피쳐 추가
    data = feature_engineering(item_data, merged_data, config)

    ### 2.5. 로스팅 포인트 단위 통일 - DB에는 변경되어 올라가므로 추후 제거
    data = change_roasting_point(data)

    ### 3. 결측치 처리
    # 콩스콩스 로스터리에서 리뷰 수가 결측인 경우는 리뷰가 없었기 때문이므로, 해당 경우는 평점과 리뷰 수를 모두 0으로 대체
    mask_idx = data[
        (data["로스터리"] == "콩스콩스") & (data["리뷰 수"].isna())
    ].index  # 리뷰가 없는 콩스콩스 상품들의 인덱스
    data.loc[mask_idx, ["리뷰 수", "평점"]] = 0

    # 나머지 리뷰 수 및 평점, 그리고 향미의 결측치들은 모두 중앙값으로 대체
    for feature_name in ["리뷰 수", "평점", "Cupping Note 향미"]:
        data = fill_to_median(data, feature_name)

    save_data(
        data,
        os.path.join(config["data_path"]),
        "preprocessed_data.csv",
    )

    return data


def save_data(data: pd.DataFrame, save_dir: str, file_name: str) -> None:
    """
    입력 받은 경로에 데이터를 저장합니다.

    Parameters
    ----------
    data : pd.DataFrame
        저장할 데이터셋

    save_dir : str
        저장할 디렉토리 경로

    file_name : str
        저장할 파일명
    """
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    file_path = os.path.join(save_dir, file_name)

    data.to_csv(file_path, index=False)


def make_item_matrix(data: pd.DataFrame, config) -> pd.DataFrame:
    """
    사용할 피쳐 선정 및 스케일링을 진행하여, 유사도 계산에 쓰일 아이템 행렬을 완성합니다.

    Parameters
    ----------
    data : pd.DataFrame
        전처리 된 아이템 데이터셋

    Returns
    -------
    pd.DataFrame : 유사도 계산에 쓰일 아이템 행렬
    """

    features_to_use = [
        "Cupping Note 향미",
        "Cupping Note 산미",
        "Cupping Note 단맛",
        "Cupping Note 바디감",
        "Roasting Point",
        "리뷰 수",
        "keywords_jaccard_similarity",
    ]
    item_matrix = data.set_index("상품명")[features_to_use].copy()
    item_matrix = scaling(item_matrix)

    save_data(
        item_matrix,
        os.path.join(config["result_path"], config["target_item_name"]),
        "item_matrix.csv",
    )

    return item_matrix


def build_item_profile(
    data: pd.DataFrame, features_to_use, config
) -> pd.DataFrame:
    """
    사용할 피쳐 선정 및 스케일링을 진행하여, 유사도 계산에 쓰일 아이템 행렬을 완성합니다.

    Parameters
    ----------
    data : pd.DataFrame
        전처리 된 아이템 데이터셋

    Returns
    -------
    pd.DataFrame : 유사도 계산에 쓰일 아이템 행렬
    """

    # features_to_use = [
    #     "Cupping Note 향미",
    #     "Cupping Note 산미",
    #     "Cupping Note 단맛",
    #     "Cupping Note 바디감",
    #     "Roasting Point",
    #     "리뷰 수",
    #     "keywords_jaccard_similarity",
    # ]
    item_profile = data[features_to_use].copy()
    item_profile = scaling(item_profile)  # 정규화
    item_profile.insert(0, "item_id", data["상품명"])

    save_data(
        item_profile,
        config["data_path"],
        "item_profile.csv",
    )

    return item_profile


def build_user_profile(inter_data, item_data, features_to_use, config):
    # 각 유저에 대한 아이템 구매 이력 리스트 생성
    item_set_for_each_user = {}
    for user_name in inter_data["구매자 이름"].unique():
        item_set_for_each_user[user_name] = set(
            inter_data[inter_data["구매자 이름"] == user_name]["상품명"]
        )

    user_profile_list = []
    user_name_list = []

    for user_name, item_set in item_set_for_each_user.items():
        items_for_each_user = item_data[
            (item_data["상품명"].isin(item_set)) & (item_data["로스터리"] == "콩스콩스")
        ][features_to_use]

        user_profile = items_for_each_user.mean().to_frame().T
        user_profile_list.append(user_profile)
        user_name_list.append(user_name)

    user_profile = pd.concat(user_profile_list, ignore_index=True)
    user_profile = scaling(user_profile)  # 정규화

    user_profile.insert(0, "user_id", user_name_list)

    save_data(user_profile, config["data_path"], "user_profile.csv")

    return user_profile


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


def change_bean_name(
    origin_bean_name: pd.Series,
) -> pd.Series:  # DB 연결 후 변경 or 제거
    """
    아이템 데이터와 통합 데이터의 병합을 위해 원두명을 통일하도록 변경합니다.
    """
    changed_bean_name = origin_bean_name.apply(
        lambda x: x.replace(" ", "")
    ).apply(lambda x: x.lower())

    return changed_bean_name


def change_roasting_point(item_data):  # DB에는 변경되어 올라가므로 추후 제거
    # 로스팅 포인트 단위 통일
    item_data.rename(
        columns={"Rosting Point": "Roasting Point"}, inplace=True
    )  # 스펠링에 오타가 있어 변경

    transform_roasting_point = {
        "미디엄 다크 로스팅": 6,
        "미디엄 로스팅": 5,
        "[시티/풀시티]": 5.5,
        "라이트 미디엄 로스팅": 4,
        "다크 로스팅": 7,
        "라이트 로스팅": 2,
        "[풀시티]": 6,
        "[시티]": 5,
        "[중볶음]": 4,
        "[하이/시티]": 4.5,
        "[중강볶음]": 5,
        "[약볶음]": 2,
        "[중볶음/중강볶음]": 4.5,
        "[풀시티/프랜치]": 6.5,
        "[하이]": 4,
        "[플시티/프렌치]": 6.5,
    }

    item_data["Roasting Point"] = item_data["Roasting Point"].map(
        transform_roasting_point
    )

    return item_data


def scaling(data: pd.DataFrame) -> pd.DataFrame:
    """
    데이터셋의 값들에 대해 최소-최대 정규화를 진행합니다.

    Parameters
    ----------
    data : pd.DataFrame
        정규화 하고자 하는 데이터셋

    Returns
    -------
    pd.DataFrame : 정규화 된 데이터셋
    """
    scaler = MinMaxScaler()
    scaled = scaler.fit_transform(data)
    data = pd.DataFrame(scaled, columns=data.columns)
    return data
