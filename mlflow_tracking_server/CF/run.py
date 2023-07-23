import os
import sys

import argparse

from utils import *
from datasets import *
from models import *
from trainers import *

from torch.utils.data import DataLoader

from datetime import datetime
import time

import mlflow


def main(args):
    now = datetime.now()
    code_dir = args.code_dir

    mlflow.set_tag("mlflow.runName", now.strftime("%Y-%m-%d / %H:%M:%S"))

    config = load_config(args)
    logger = init_logger()

    seed_everything(config["seed"])

    logger.info("|| Load data")
    inters = load_interaction()
    items = inters["item"].unique()

    dataset_params = config["dataset_params"]
    origin, train, test, num_users, num_items = preprocess_for_train(
        inters.copy(),
        dataset_params,
        code_dir,
        feedback_type=config["feedback_type"],
    )

    sparsity = (
        round((origin == 0).sum() / (origin.shape[0] * origin.shape[1]), 4)
        * 100
    )
    logger.info(f"|| Sparsity : {sparsity}%")
    mlflow.log_param("sparsity", sparsity)

    if "num_users" in config["model_params"].keys():
        config["model_params"]["num_users"] = num_users
        config["model_params"]["num_items"] = num_items
    else:
        config["dataset_params"]["num_users"] = num_users
        config["dataset_params"]["num_items"] = num_items

    for key, value in zip(list(config.keys()), list(config.values())):
        if key[-6::] == "params":
            for key_, value_ in zip(list(value.keys()), list(value.values())):
                mlflow.log_param(key_, value_)
        else:
            mlflow.log_param(key, value)

    logger.info("|| Initialize dataset")
    dataset = get_dataset(config)
    # origin_dataset = dataset(data=origin)
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
        # trainer = trainer(
        #     model, origin_dataset, test_dataset, logger, config=trainer_params
        # )

    logger.info("|| Train model")
    best_model, best_rmse, best_epoch = trainer.run()

    test_num = int(len(inters) * dataset_params["test_ratio"])
    test_users = np.random.choice(inters["user"].unique(), test_num)

    test_inters = inters[inters["user"].isin(test_users)].reset_index(drop=True)
    test_users = test_inters["user"].unique()
    test_items = test_inters["item"].unique()

    final_test, user_enc, item_enc = preprocess_for_inference(
        test_inters.copy(), code_dir, feedback_type=config["feedback_type"]
    )

    final_test_dataset = dataset(data=final_test)
    final_test_loader = None

    if config["dataset"] == "TorchDataset":
        final_test_loader = DataLoader(
            final_test_dataset,
            batch_size=len(final_test_dataset),
            shuffle=False,
            num_workers=0,
        )

    recommended_items = best_model.predict(
        test_inters,
        user_enc,
        item_enc,
        test_users,
        test_items,
        config["topk"],
        final_test_loader,
    )

    mean_precision = round(get_precision(test_inters, recommended_items), 4)
    logger.info(f"|| precision@{config['topk']} : {mean_precision}")

    mlflow.log_metric("best_rmse", best_rmse)
    mlflow.log_metric("best_epoch", best_epoch)
    mlflow.log_metric("mean_precision", mean_precision)

    logger.info("|| Save model")
    save_model(best_model, config, code_dir)

    artifacts = {"model_path": f"{config['model']}_{config['config_name']}.pkl"}

    mlflow.pyfunc.log_model(
        artifact_path=config["model"],
        # loader_module=None,
        # data_path=None,
        code_path=[
            "./datasets.py",
            "./models.py",
            "./trainers.py",
            "./utils.py",
        ],
        python_model=Wrapper(code_dir, config, items),
        # registered_model_name=None,
        artifacts=artifacts,
    )


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
    parser.add_argument(
        "--code_dir",
        "-cd",
        type=str,
        default="/opt/ml/Recommendation-Modeling/mlflow_tracking_server/CF",
        help="path of running code",
    )

    args = parser.parse_args()
    main(args)
