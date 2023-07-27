import pickle

from typing import Tuple

import numpy as np
import pandas as pd

import scipy
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split

import torch
from torch.utils.data import Dataset

from sqlalchemy import create_engine


def load_table(query: str) -> pd.DataFrame:
    """
    query : SQL query
    """
    URL = "postgresql+psycopg2://yerim:yerim@101.101.210.35:30005/djangodb"
    engine = create_engine(URL, echo=False)

    table = pd.read_sql_query(query, con=engine)

    return table


# fix or remove
def load_user_cluster_interaction(data_path: str) -> pd.DataFrame:
    """
    data_path : interaction 데이터 csv 경로
    """
    inters = pd.read_csv(data_path)
    inters.columns = ["user", "item", "rating"]

    return inters


def load_interaction() -> pd.DataFrame:
    """
    Entity Linking으로 유저를 식별해 interaction 데이터를 구성
    """
    load_all_reviews_query = "select * from coffee_bean_beanreview"
    data = load_table(load_all_reviews_query)

    data = data[data["user_nickname"] != "쿠팡실구매자"].reset_index(drop=True)

    filtered_users = []

    more_inter_users_idx = np.where(data["user_nickname"].value_counts() > 1)[0]
    more_inter_users_name = (
        data["user_nickname"].value_counts()[more_inter_users_idx].keys()
    )
    more_inter_data = data[
        data["user_nickname"].isin(more_inter_users_name)
    ].reset_index(drop=True)

    for name in more_inter_data["user_nickname"].unique():
        if not (((len(name) == 3) | (len(name) == 2)) & ("*" in name)):
            filtered_users.append(name)

    one_inter_users_idx = np.where(data["user_nickname"].value_counts() == 1)[
        0
    ]  # interacion 1개인 유저 제외?
    one_interact_users = (
        data["user_nickname"]
        .value_counts()[one_inter_users_idx]
        .keys()
        .tolist()
    )

    filtered_users = filtered_users + one_interact_users
    filtered_data = data[
        data["user_nickname"].isin(filtered_users)
    ].reset_index(drop=True)

    inters = filtered_data[["user_nickname", "bean_id_id", "rating"]]
    inters.columns = ["user", "item", "rating"]

    return inters


def load_encoders(encoder_path: str) -> Tuple:
    """
    encoder_path : 학습된 LabelEncoder pickle 파일 경로
    """
    with open(f"{encoder_path}/user_info.pkl", "rb") as file:
        user_info = pickle.load(file)
        user_enc = user_info["encoder"]
        num_users = user_info["num_users"]

    with open(f"{encoder_path}/item_info.pkl", "rb") as file:
        item_info = pickle.load(file)
        item_enc = item_info["encoder"]
        num_items = item_info["num_items"]

    return user_enc, item_enc, num_users, num_items


def save_encoders(
    user_encoder: LabelEncoder,
    item_encoder: LabelEncoder,
    num_users: int,
    num_items: int,
    encoder_path: str,
) -> None:
    """
    user_encoder : 학습된 User LabelEncoder
    item_encoder : 학습된 Item LabelEncoder
    num_users : 학습 데이터 user 수
    num_items : 학습 데이터 item 수
    encoder_path : 학습된 LabelEncoder pickle 파일 저장 경로
    """
    user_info = {"encoder": user_encoder, "num_users": num_users}
    item_info = {"encoder": item_encoder, "num_items": num_items}

    # fix below (FileNotFoundError: [Errno 2] No such file or directory: './saved/user_info.pkl')
    with open(f"{encoder_path}/user_info.pkl", "wb") as file:
        pickle.dump(user_info, file)
    with open(f"{encoder_path}/item_info.pkl", "wb") as file:
        pickle.dump(item_info, file)


def preprocess_for_train(
    data: pd.DataFrame, config
) -> Tuple[np.ndarray, np.ndarray, int, int]:
    r"""Helper function to preprocess data.

    Parameters
    ----------
    data : pd.DataFrame
        dataset which consists of user, item, rating columns.

    Returns
    -------
    Tuple[np.ndarray, np.ndarray, int, int]
    """
    num_users = data["user"].nunique()
    num_items = data["item"].nunique()

    user_enc = LabelEncoder()
    item_enc = LabelEncoder()

    # Every user and item would be used as index
    data["user"] = user_enc.fit_transform(data["user"])
    data["item"] = item_enc.fit_transform(data["item"])

    data["user"] -= 1
    data["item"] -= 1

    train, test = train_test_split(data.values, test_size=config["test_ratio"])
    origin = data.values

    train_mat = np.zeros((num_users, num_items))
    test_mat = np.zeros((num_users, num_items))
    origin_mat = np.zeros((num_users, num_items))

    for user, item, rating in train:
        train_mat[user, item] = rating
    for user, item, rating in test:
        test_mat[user, item] = rating
    for user, item, rating in origin:
        origin_mat[user, item] = rating

    train_mat /= 5
    test_mat /= 5
    origin_mat /= 5

    save_encoders(user_enc, item_enc, num_users, num_items, "./saved")  # fix
    return origin_mat, train_mat, test_mat, num_users, num_items


def preprocess_for_inference(
    data: pd.DataFrame,
) -> Tuple[np.ndarray, np.ndarray, int, int]:
    r"""Helper function to preprocess data.

    Parameters
    ----------
    data : pd.DataFrame
        dataset which consists of user, item, rating columns.

    Returns
    -------
    Tuple[np.ndarray, np.ndarray, int, int]
    """

    user_enc, item_enc, num_users, num_items = load_encoders("./saved")  # fix

    # Every user and item would be used as index
    data["user"] = user_enc.transform(data["user"])
    data["item"] = item_enc.transform(data["item"])

    # data["user"] -= 1
    # data["item"] -= 1

    data = data.values
    output = np.zeros((num_users, num_items))

    for user, item, rating in data:
        output[user, item] = rating
    for user, item, rating in data:
        output[user, item] = rating

    output /= 5

    return output, user_enc, item_enc


class BaseDataset:
    """
    Parameters
    ----------
    data : np.ndarray
        A two-dimensional list is required.
    """

    def __init__(self, data: np.ndarray) -> None:
        self.data = data
        self.items = set(data.nonzero()[0])
        self.users = set(data.nonzero()[1])

    def __len__(self) -> int:
        return len(self.data)

    def __getitem__(self, index) -> None:
        return self.data[index]


class TorchDataset(BaseDataset, Dataset):
    def __init__(self, data: np.ndarray) -> None:
        super(TorchDataset, self).__init__(data)
