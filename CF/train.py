import os
import sys

import argparse

from utils.utils import *
from utils.datasets import *
from utils.models import *
from utils.trainers import *

from torch.utils.data import DataLoader

sys.path.append("./utils")


def main(args):
    config = load_config(args)
    logger = init_logger()  # 아직 사용하지 않음

    seed_everything(config["seed"])

    logger.info("|| Load data")
    inters = load_user_cluster_interaction(config["data_path"])

    dataset_params = config["dataset_params"]
    train, test, num_users, num_items = preprocess_for_train(
        inters.copy(), dataset_params
    )

    if "num_users" in config["model_params"].keys():
        config["model_params"]["num_users"] = num_users
        config["model_params"]["num_items"] = num_items

    logger.info("|| Initialize dataset")
    dataset = get_dataset(config)
    train_dataset = dataset(data=train)
    test_dataset = dataset(data=test)

    if config["dataset"] == "TorchDataset":
        train_loader = DataLoader(
            train_dataset,
            batch_size=dataset_params["batch_size"],
            shuffle=dataset_params["shuffle"],
        )
        test_loader = DataLoader(
            test_dataset,
            batch_size=len(test_dataset),
            shuffle=False,
            num_workers=0,
        )

    logger.info("|| Initialize model")
    model = get_model(config)
    model_params = config["model_params"]
    model = model(config=model_params)

    logger.info("|| Initialize trainer")
    trainer = get_trainer(config)
    trainer_params = config["trainer_params"]
    if trainer_params["device"] == "cuda":
        model.to("cuda")

    if config["dataset"] == "TorchDataset":
        trainer = trainer(
            model,
            train_dataset,
            test_dataset,
            train_loader,
            test_loader,
            logger,
            config=trainer_params,
        )
    else:
        trainer = trainer(
            model, train_dataset, test_dataset, logger, config=trainer_params
        )

    logger.info("|| Train model")
    trainer.run()

    logger.info("|| Save model")
    save_model(model, config)


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
