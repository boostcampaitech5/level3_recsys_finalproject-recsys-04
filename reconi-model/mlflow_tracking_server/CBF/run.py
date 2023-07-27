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


def main(args):
    now = datetime.now()
    mlflow.set_tag("mlflow.runName", now.strftime("%Y-%m-%d / %H:%M:%S"))

    # -- config 설정 정보 로드
    config = load_config(args)

    # -- 예측 인스턴스 생성 및 저장
    predictor = CosineSimilarityRec(config)

    with open(f"CBF_{config['config_name']}.pkl", "wb") as file:
        pickle.dump(predictor, file)

    # cosine similarity 1개 (not cold start) pickle 저장
    all_item_profile = load_item_profile(all=True)
    # ksks_item_profile = item_profile[item_profile["roastery"] == "콩스콩스"]
    cosine_sim_df = predictor.save_cosine_sim(
        all_item_profile,
    )

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
