import os

import numpy as np
import pandas as pd

from sklearn.metrics.pairwise import cosine_similarity

from typing import Tuple, Optional

import time

import mlflow

from data import load_data
import pickle


class Wrapper(mlflow.pyfunc.PythonModel):
    def __init__(self, config):
        self.config = config

    def load_context(self, context):
        with open(context.artifacts["predictor_path"], "rb") as file:
            self.predictor = pickle.load(file)

    def predict(self, context, model_input):
        config = self.config

        self.predictor.user_profile = model_input.drop(columns="user_id")
        self.predictor.user_ids = model_input["user_id"]

        start_time = time.time()
        target_name, preds = self.predictor.recommend()
        end_time = time.time()

        print(f"|| Inference time : {round(end_time - start_time, 4)}")

        return preds


class CosineSimilarityRec:
    def __init__(
        self, config, data, item_ids, user_ids, item_profile, user_profile
    ):
        self.config = config
        self.data = data
        self.item_ids = item_ids
        self.user_ids = user_ids
        self.item_profile = item_profile
        self.user_profile = user_profile

    def recommend(self):
        config = self.config
        data = self.data
        item_ids = self.item_ids
        user_ids = self.user_ids
        item_profile = self.item_profile
        user_profile = self.user_profile

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
            (
                recommendation_result,
                recommended_items_df,
            ) = get_recommendation_result(
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
            (
                recommendation_result,
                recommended_items_df,
            ) = get_recommendation_result(
                config, config["target_user_name"], cosine_sim_df, data
            )

            # 추천 결과 저장 경로
            save_dir = os.path.join(
                config["result_path"],
                "target_user_based",
                config["target_user_name"],
            )

        # 결과 기록
        # target_name = config["target_item_name"]

        return target_name, recommendation_result


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
    if config["target_item_name"]:
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

    else:
        recommendation_result = {
            "target_user_name": target_name_list,
            "recommended_item_name": recom_name,
            "recommended_item_roastery": recom_roastery,
            "cosine_similarity": cosine_similarity,
        }

    return pd.DataFrame(recommendation_result), recommended_items_df
