import os

import numpy as np
import pandas as pd

import argparse
from typing import Tuple, Optional

from datetime import datetime
import mlflow
import time

from data import load_config  # , load_data
from predictor import CosineSimilarityRec, Wrapper

import pickle


def main(args):
    now = datetime.now()
    mlflow.set_tag("mlflow.runName", now.strftime("%Y-%m-%d / %H:%M:%S"))

    # -- config 설정 정보 로드
    config = load_config(args)

    # -- 예측 인스턴스 생성 및 저장
    predictor = CosineSimilarityRec(config)

    with open(f"CBF_{config['config_name']}.pkl", "wb") as file:
        pickle.dump(predictor, file)

    # -- 예측 결과
    topk, mean_cosine_sim = predictor.get_recom_result()

    mlflow.log_param("topk", topk)
    # mlflow.log_metric( # 예측 전 계산이 되지 않으므로 저장 불가
    #     "mean_cosine_similarity",
    #     mean_cosine_sim,
    # )

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
