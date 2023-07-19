import os

import numpy as np
import pandas as pd

from sklearn.metrics.pairwise import cosine_similarity

import argparse
from typing import Tuple, Optional

from datetime import datetime
import mlflow

from data import load_config, load_data, save_data, validate_config


def main(args):
    # mlflow 설정
    now = datetime.now()
    mlflow.set_tag("mlflow.runName", now.strftime("%Y-%m-%d / %H:%M:%S"))

    # config 설정 정보 및 데이터 로드
    config = load_config(args)
    if not validate_config(config):
        return

    data, item_profile, user_profile = load_data(config)

    item_ids = item_profile["item_id"]
    user_ids = user_profile["user_id"]
    item_profile = item_profile.iloc[:, 1:]
    user_profile = user_profile.iloc[:, 1:]

    # 타겟 아이템 기반 추천
    if config["target_item_name"]:
        target_name = config["target_item_name"]

        # 코사인 유사도 계산
        cosine_sim = cosine_similarity(item_profile)

        cosine_sim_df = pd.DataFrame(
            cosine_sim,
            index=item_ids,
            columns=item_ids,
        )

        # 유사도 기반 추천
        recommendation_result, recommended_items_df = get_recommendation_result(
            config,
            config["target_item_name"],
            cosine_sim_df,
            data,
            config["topk"],
        )

        # 추천 결과 저장 경로
        save_dir = os.path.join(
            config["result_path"],
            "target_item_based",
            config["target_item_name"],
        )

    # 타겟 유저 기반 추천
    else:
        target_name = config["target_user_name"]

        # 코사인 유사도 계산
        cosine_sim = cosine_similarity(item_profile, user_profile)

        cosine_sim_df = pd.DataFrame(
            cosine_sim,
            index=item_ids,
            columns=user_ids,
        )

        # 유사도 기반 추천
        recommendation_result, recommended_items_df = get_recommendation_result(
            config, config["target_user_name"], cosine_sim_df, data
        )

        # 추천 결과 저장 경로
        save_dir = os.path.join(
            config["result_path"],
            "target_user_based",
            config["target_user_name"],
        )

    print(recommendation_result)

    save_data(  # 추천된 아이템과 유사도 값만을 저장하는 요약 결과 저장
        recommendation_result,
        save_dir,
        "summary_results.csv",
    )
    save_data(  # 추천된 아이템의 모든 정보 저장
        recommended_items_df,
        save_dir,
        "recommended_items.csv",
    )

    # 결과 기록
    topk = config["topk"]

    mlflow.log_param("target_name", target_name)
    mlflow.log_param("topk", topk)
    mlflow.log_metric(
        "mean_cosine_similarity",
        recommendation_result["cosine_similarity"].mean(),
    )


def get_recommendation_result(
    config,
    target_name: str,
    similarity_matrix: pd.DataFrame,
    items: pd.DataFrame,
    k: Optional[int] = 5,
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    콘텐츠 기반 필터링 추천 결과를 얻을 수 있습니다.

    Parameters
    ----------
    config : 데이터 경로 등의 설정 정보

    target_name : str
        타겟 아이템의 이름

    similarity_matrix : pd.DataFrame
        유사도 행렬

    items : pd.DataFrame
        아이템 정보 행렬

    k : Optional[int] = 5
        상위 k개의 아이템을 추천 (기본값: 5)

    Returns
    -------
    Tuple[pd.DataFrame, pd.DataFrame] : 추천 요약 결과 데이터셋과, 추천된 아이템 정보 데이터셋
    """
    recom_idx = (
        similarity_matrix.loc[:, target_name]
        .values.reshape(1, -1)
        .argsort()[:, ::-1]
        .flatten()[1 : k + 1]
    )

    recom_name = items.iloc[recom_idx, :]["상품명"].values
    recom_roastery = items.iloc[recom_idx, :]["로스터리"].values
    cosine_similarity = similarity_matrix.iloc[recom_idx][target_name].values
    recommended_items_df = items.iloc[recom_idx, :]

    target_name_list = np.full(len(range(k)), target_name)

    if config["target_item_name"]:  # 타겟 아이템 기반 추천
        target_roastery_list = np.full(
            len(range(k)), items[items["상품명"] == target_name]["로스터리"].values
        )

        recommendation_result = {
            "target_item_name": target_name_list,
            "target_item_roastery": target_roastery_list,
            "recommended_item_name": recom_name,
            "recommended_item_roastery": recom_roastery,
            "cosine_similarity": cosine_similarity,
        }

    else:  # 타겟 유저 기반 추천
        recommendation_result = {
            "target_user_name": target_name_list,
            "recommended_item_name": recom_name,
            "recommended_item_roastery": recom_roastery,
            "cosine_similarity": cosine_similarity,
        }

    return pd.DataFrame(recommendation_result), recommended_items_df


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--config_name",
        "-c",
        type=str,
        default="baseline",
        help="specific name of config to use",
    )

    args = parser.parse_args()
    main(args)
