import os

import numpy as np
import pandas as pd

import argparse
from typing import Tuple, Optional

from datetime import datetime
import mlflow
import time

from data import load_config, load_item_profile
from predictor import CosineSimilarityRec, Wrapper

import pickle

from utils import Evaluator

import warnings

warnings.filterwarnings("ignore")


def main(args):
    now = datetime.now()
    mlflow.set_tag("mlflow.runName", now.strftime("%Y-%m-%d / %H:%M:%S"))

    # -- config 설정 정보 로드
    config = load_config(args)

    # -- item-item cosine similarity 저장
    all_item_profile = load_item_profile(all=True, force_keyword_feature=True)

    # -- 예측 인스턴스 생성 및 저장
    predictor = CosineSimilarityRec(config, all_item_profile)

    with open(f"CBF_{config['config_name']}.pkl", "wb") as file:
        pickle.dump(predictor, file)

    cosine_sim_df = predictor.save_cosine_sim(
        all_item_profile,
    )

    # -- 평가 metrics
    all_item_profile.iloc[:, 1:6] = (
        all_item_profile.iloc[:, 1:6] * 10
    )  # 스케일링 제거 (원본값으로 복원)

    evaluator = Evaluator(config, predictor, all_item_profile)

    # 평균 유클리디안 거리: 유저 인풋과 예측값 간 유클리디안 거리 평균 -> 작을수록 유저 인풋과 유사한 예측을 냄을 의미
    mean_euclidean_dist = round(evaluator.get_euclidean_distance(), 5)
    print("mean_euclidean_dist: ", mean_euclidean_dist)
    mlflow.log_param("mean euclidean distance", mean_euclidean_dist)

    # entropy: 추천되는 아이템의 다양성 평균 -> 같은 추천 리스트 내 같은 아이템이 많을수록(다양하지 않을수록) 값이 작아짐
    entropy_diversity = round(evaluator.get_entropy_diversity(), 5)
    print("entropy_diversity: ", entropy_diversity)
    mlflow.log_param("entropy diversity", entropy_diversity)

    # diversity: 전체 아이템 중 추천된 고유 아이템의 비율 -> 모든 추천에 걸쳐 추천되는 아이템이 다양할수록 값이 높음
    diversity = round(evaluator.get_diversity(), 5)
    print("diversity: ", diversity)
    mlflow.log_param("diversity", diversity)

    # -- mlflow 기록
    artifacts = {
        "predictor_path": f"CBF_{config['config_name']}.pkl",
        "cos_sim_path": f"item-item_cosine_sim.pkl",
    }

    mlflow.pyfunc.log_model(
        artifact_path="CBF",
        code_path=[
            "./data.py",
            "./feature_engineering.py",
            "./predictor.py",
        ],
        python_model=Wrapper(config, predictor, cosine_sim_df),
        artifacts=artifacts,
    )


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
