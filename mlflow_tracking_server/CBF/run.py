import os

import numpy as np
import pandas as pd

from sklearn.metrics.pairwise import cosine_similarity

import argparse
from typing import Tuple, Optional

from datetime import datetime
import mlflow
import time

from data import load_config, load_data, save_data, validate_config
from predictor import *

import pickle


def main(args):
    # mlflow 설정
    now = datetime.now()
    mlflow.set_tag("mlflow.runName", now.strftime("%Y-%m-%d / %H:%M:%S"))

    # config 설정 정보 및 데이터 로드
    config = load_config(args)

    data, item_profile, user_profile = load_data(config)

    item_ids = item_profile["item_id"]
    user_ids = user_profile["user_id"]
    item_profile = item_profile.iloc[:, 1:]
    user_profile = user_profile.iloc[:, 1:]

    predictor = CosineSimilarityRec(
        config, data, item_ids, user_ids, item_profile, user_profile
    )

    with open(f"CBF_{config['config_name']}.pkl", "wb") as file:
        pickle.dump(predictor, file)

    topk = config["topk"]

    target_name, recommendation_result = predictor.recommend()

    mlflow.log_param("target_name", target_name)
    mlflow.log_param("topk", topk)
    mlflow.log_metric(
        "mean_cosine_similarity",
        recommendation_result["cosine_similarity"].mean(),
    )

    artifacts = {"predictor_path": f"CBF_{config['config_name']}.pkl"}

    mlflow.pyfunc.log_model(
        artifact_path="CBF",
        code_path=[
            "./data.py",
            "./feature_engineering.py",
            "./predictor.py",
        ],
        python_model=Wrapper(config),
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
