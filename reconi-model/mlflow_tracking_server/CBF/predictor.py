import os

import numpy as np
import pandas as pd

from sklearn.metrics.pairwise import cosine_similarity

from typing import Tuple, Optional

import time

import mlflow

import pickle

from data import load_item_profile


class Wrapper(mlflow.pyfunc.PythonModel):
    def __init__(self, config, predictor, cosine_sim):
        self.config = config
        self.predictor = predictor
        self.cosine_sim = cosine_sim

    def predict(self, context, model_input):
        # -- cold start (recommend for target user)
        if isinstance(model_input, pd.DataFrame):
            self.predictor.user_preferences = model_input  # dataframe

            start_time = time.time()
            preds = self.predictor.recommend_for_target_user()[
                0
            ]  # 직접 입력 받는 유저는 항상 1명이므로 항상 0번째 컬럼을 가져옴
            end_time = time.time()

        # -- not cold start (recommend for target item)
        else:
            model_input = list(model_input)
            self.predictor.target_item_ids = model_input  # list

            start_time = time.time()
            preds = self.predictor.recommend_for_target_item(self.cosine_sim)
            end_time = time.time()

        print(f"|| Inference time : {round(end_time - start_time, 4)}")

        return preds


class CosineSimilarityRec:
    def __init__(self, config, item_profile):
        self.topk = config["topk"]
        self.item_profile = item_profile
        # self.mean_cosine_sim = None

    # -- cold start (recommend for target user)
    def recommend_for_target_user(self):
        item_profile = self.item_profile
        user_preferences = self.user_preferences
        k = self.topk

        # 코사인 유사도 계산
        cosine_sim = cosine_similarity(
            item_profile.drop("id", axis=1), user_preferences
        )
        cosine_sim_df = pd.DataFrame(
            cosine_sim,
            index=item_profile["id"],
        )

        # 유사도 기반 추천
        recom_items_list = []
        for i in range(len(user_preferences)):
            recom_idx = (
                cosine_sim_df.loc[:, i]
                .values.reshape(1, -1)
                .argsort()[:, ::-1]
                .flatten()[1 : k + 1]  # top k
            )
            recom_item_ids = item_profile.iloc[recom_idx, :]["id"].values
            recom_items_list.append(recom_item_ids)

        return recom_items_list

    # -- not cold start (recommend for target item)
    def recommend_for_target_item(self, cosine_sim, is_saved: bool = False):
        target_item_ids = self.target_item_ids
        self.item_profile = load_item_profile(target_item_ids)
        item_profile = self.item_profile

        # 코사인 유사도 계산
        # cosine_sim_df = self.load_cosine_sim()
        cosine_sim_df = cosine_sim[target_item_ids]

        # 유사도 기반 추천
        # 자기 자신(id)과의 유사도는 무조건 1이므로, 해당 행 -inf 로 대체
        cosine_sim_df = (
            cosine_sim_df.reset_index(drop=True).round(5).replace(1, -np.inf)
        )
        # 각 item의 top 1 item을 가져옴
        recom_idx = cosine_sim_df.idxmax().tolist()

        recom_item_ids = item_profile.iloc[recom_idx, :]["id"].values

        return recom_item_ids

    def load_cosine_sim(self):
        with open("item-item_cosine_sim.pkl", "rb") as file:
            return pickle.load(file)

    def save_cosine_sim(self, item_profile):
        cosine_sim = cosine_similarity(
            item_profile.drop("id", axis=1),
        )

        cosine_sim_df = pd.DataFrame(
            cosine_sim, index=item_profile["id"], columns=item_profile["id"]
        )

        with open("item-item_cosine_sim.pkl", "wb") as file:
            pickle.dump(cosine_sim_df, file)

        with open("../CF/item-item_cosine_sim.pkl", "wb") as file:
            pickle.dump(cosine_sim_df, file)

        return cosine_sim_df

    def get_recom_result(self):
        return self.topk
