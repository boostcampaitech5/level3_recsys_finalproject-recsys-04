import os
import sys

import importlib
import yaml

import random

import numpy as np
import pandas as pd

import torch

import pickle
import logging


def load_config(args):
    with open(f"{args.code_dir}/{args.model}.yaml") as f:
        config = yaml.load(f, Loader=yaml.FullLoader)
        config = config[f"{args.config_name}"]
        print("----- config -----")
        print(config)
        print("--------------------")

    return config


def seed_everything(seed: int = 42):
    random.seed(seed)
    np.random.seed(seed)
    os.environ["PYTHONHASHSEED"] = str(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed(seed)  # type: ignore
    torch.backends.cudnn.deterministic = True  # type: ignore
    torch.backends.cudnn.benchmark = True  # type: ignore


def get_dataset(config):
    try:
        module_name = "datasets"
        dataset = importlib.import_module(module_name)
        dataset = getattr(dataset, config["dataset"])
        return dataset

    except ImportError:
        print(f"Module '{module_name}' not found")
    except AttributeError:
        print(
            f"Class '{config['dataset']}' not found in module '{module_name}'"
        )


def get_model(config):
    try:
        module_name = "models"
        model = importlib.import_module(module_name)
        model = getattr(model, config["model"])
        return model

    except ImportError:
        print(f"Module '{module_name}' not found")
    except AttributeError:
        print(f"Class '{config['model']}' not found in module '{module_name}'")


def get_trainer(config):
    try:
        module_name = "trainers"
        trainer = importlib.import_module(module_name)
        trainer = getattr(trainer, config["trainer"])
        return trainer

    except ImportError:
        print(f"Module '{module_name}' not found")
    except AttributeError:
        print(
            f"Class '{config['trainer']}' not found in module '{module_name}'"
        )


def get_precision(
    actual_inters: pd.DataFrame, recommended_items: pd.DataFrame
) -> int:
    """
    actual : 실제 유저의 interaction
    recommended : 추천된 유저의 interaction 형식의 추천 아이템 result
    """

    precisions = []

    for actual_items, recommended_items in zip(
        actual_inters.groupby("user")["item"].unique(),
        recommended_items.groupby("user")["item"].unique(),
    ):
        intersection = set(actual_items).intersection(set(recommended_items))
        precision = len(intersection) / len(recommended_items)

        precisions.append(precision)

    return np.mean(precisions)


def save_model(model, config, code_dir):
    # os.makedirs(f"./saved/{config['model']}", exist_ok=True)
    # with open(
    #     f"./saved/{config['model']}/{config['config_name']}.pkl", "wb"
    # ) as file:
    with open(
        f"{code_dir}/{config['model']}_{config['config_name']}.pkl",
        "wb",
    ) as file:
        pickle.dump(model, file)


### artifact 사용하지 않을 때
# def load_model(config, code_dir):
#     with open(
#         f"{code_dir}/{config['model']}_{config['config_name']}.pkl",
#         "rb",
#     ) as file:
#         model = pickle.load(file)

#     return model


def load_model(path):
    with open(path, "rb") as file:
        model = pickle.load(file)

    return model


def init_logger():
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    log_handler = logging.StreamHandler()
    log_handler.setLevel(logging.INFO)
    formatter = logging.Formatter("%(asctime)s %(levelname)s:%(message)s")
    log_handler.setFormatter(formatter)

    logger.addHandler(log_handler)

    return logger
