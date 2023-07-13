import os
import sys

import argparse

from utils.utils import *
from utils.datasets import *
from utils.models import *
from utils.trainers import *

from torch.utils.data import DataLoader

import warnings

warnings.filterwarnings("ignore")

sys.path.append("./utils")


def main(args):
    config = load_config(args)
    logger = init_logger()  # 아직 사용하지 않음

    seed_everything(config["seed"])

    logger.info("|| Load data")
    # 새로 들어오는 유저 interaction 으로 바꾸어야 함
    inters = load_user_cluster_interaction(config["data_path"])
    # 현재는 toy data
    items = inters["item"].unique()
    inters = inters[inters["user"] == 4]

    users = inters["user"].unique()

    output, user_enc, item_enc = preprocess_for_inference(inters.copy())

    logger.info("|| Initialize dataset")
    dataset = get_dataset(config)
    dataset = dataset(data=output)

    if config["dataset"] == "TorchDataset":
        loader = DataLoader(
            dataset,
            batch_size=len(dataset),
            shuffle=False,
            num_workers=0,
        )
    else:
        loader = None

    logger.info("|| Load model")
    model = load_model(config)

    logger.info("|| Inference")
    preds = model.predict(
        inters, user_enc, item_enc, users, items, config["topk"], loader=loader
    )

    # print(f"result: {preds['item'].values}")  # 저장되도록 바꾸어야 함
    logger.info(f"|| Result \n{preds.reset_index(drop=True)}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", "-m", type=str, help="name of model to use")
    parser.add_argument(
        "--config_name",
        "-c",
        type=str,
        default="baseline",
        help="specific name of config to use",
    )

    args = parser.parse_args()
    main(args)
