import numpy as np
import pandas as pd

from sklearn.preprocessing import LabelEncoder
from multiprocessing import Pool, cpu_count

from scipy.sparse import csr_matrix

import torch
import torch.nn as nn
from torch.utils.data import DataLoader

import time

from utils import *
from datasets import *

import mlflow

import warnings

warnings.filterwarnings("ignore")


class Wrapper(mlflow.pyfunc.PythonModel):
    def __init__(self, code_dir, config, items, inters):
        super(Wrapper, self).__init__()
        self.code_dir = code_dir
        self.config = config
        self.items = items
        self.inters = inters

    def load_context(self, context):
        self.model = load_model(context.artifacts["model_path"])
        self.cosine_sim = load_cosine_sim(context.artifacts["cosine_sim_path"])

    def predict(self, context, model_input):
        logger = init_logger()

        start_time = time.time()
        preds = self.custom_predict(logger, model_input)
        end_time = time.time()

        logger.info(f"|| Inference time : {round(end_time - start_time, 4)}")
        logger.handlers.clear()

        return preds

    def custom_predict(self, logger, model_input):
        code_dir = self.code_dir
        config = self.config
        items = self.items
        origin_inters = self.inters

        new_inters = model_input
        new_users = new_inters["user"].unique()

        logger.info(f"|| Access users : {new_users}")

        ksks_ids = [i for i in range(0, 42)]  # 콩스콩스 아이템 id
        ksks_matched_items = dict(self.cosine_sim.loc[ksks_ids, :].idxmax())

        # CBF (any item -> ksks item)
        new_inters.loc[:, "item"] = new_inters["item"].apply(
            lambda x: ksks_matched_items[x]
        )

        # CF
        if config["model"] == "EASE":
            inters = pd.concat([origin_inters, new_inters]).reset_index(
                drop=True
            )
        else:
            inters = new_inters

        inters_copy = inters.copy()

        items = inters_copy["item"].unique()

        num_users = inters_copy["user"].nunique()
        num_items = len(ksks_ids)
        # num_items = inters_copy["item"].nunique()

        user_enc = LabelEncoder()
        item_enc = LabelEncoder()

        # Every user and item would be used as index
        inters_copy["user"] = user_enc.fit_transform(inters_copy["user"])
        inters_copy["item"] = item_enc.fit_transform(inters_copy["item"])

        data = inters_copy.values
        output = np.zeros((num_users, num_items))

        for user, item, rating in data:
            output[user, item] = rating

        output /= 5

        if config["feedback_type"] == "implicit":
            output[np.where(output > 0)] = 1

        dataset = get_dataset(config)
        dataset = dataset(data=output)

        loader = None
        if config["dataset"] == "TorchDataset":
            loader = DataLoader(
                dataset,
                batch_size=len(dataset),
                shuffle=False,
                num_workers=0,
            )

        if config["model"] == "EASE":
            self.model.fit(dataset.data)

        preds = self.model.predict(
            inters,
            user_enc,
            item_enc,
            new_users,
            items,
            config["topk"],
            loader=loader,
        ).reset_index(drop=True)

        # CBF (ksks item -> any item)
        ksks_rec_items = preds["item"].tolist()

        any_rec_items = (
            self.cosine_sim.loc[
                list(set(self.cosine_sim.index) - set(ksks_ids)), ksks_rec_items
            ]
            .idxmax()
            .values
        )

        preds["score"] = any_rec_items
        preds.columns = ["user", "ksks_item", "any_item"]

        result = {}
        for user, group_values in preds.groupby("user"):
            result[f"{user}"] = (
                group_values[["ksks_item", "any_item"]]
                .values.flatten()
                .tolist()
            )

        return result


class BaseModel:
    def predict(
        self,
        new_df: pd.DataFrame,
        user_enc: LabelEncoder,
        item_enc: LabelEncoder,
        users: np.ndarray,
        items: np.ndarray,
        k: int,
        loader: torch.utils.data.DataLoader,
    ):
        """
        user_enc : 유저 인코딩에 사용한 LabelEncoder 객체
        item_enc : 아이템 인코딩에 사용한 LabelEncoder 객체
        new_df : inters 데이터프레임
        users : user 의 unique array
        items : item 의 unique array
        k : 몇 개의 추천을 받을 것인지
        loader : 필요한 경우 torch DataLoader 입력
        """
        items = item_enc.transform(items)
        dd = new_df.loc[new_df.user.isin(users)]
        dd["ci"] = item_enc.transform(dd.item)
        dd["cu"] = user_enc.transform(dd.user)
        g = dd.groupby("cu")

        if loader is not None:
            pred = next(iter(loader)).cuda().to(torch.float32)
            pred = self.forward(pred)
            self.pred = pred.detach().cpu().numpy()

        with Pool(cpu_count()) as p:
            user_preds = p.starmap(
                self.predict_for_user,
                [
                    (user, group, self.pred[user, :], items, k)
                    for user, group in g
                ],
            )

        df = pd.concat(user_preds)
        df["item"] = item_enc.inverse_transform(df["item"])
        df["user"] = user_enc.inverse_transform(df["user"])
        df["score"] = df["score"].round(4)
        return df

    @staticmethod
    def predict_for_user(user, group, pred, items, k):
        # watched = set(group["ci"])  ### 본 것도 추천 하려면 이 부분 주석!
        watched = set()
        candidates = [item for item in items if item not in watched]
        pred = np.take(pred, candidates)
        pred = (pred - min(pred)) / (max(pred) - min(pred))

        res = np.argpartition(pred, -k)[-k:]
        r = pd.DataFrame(
            {
                "user": [user] * len(res),
                "item": np.take(candidates, res),
                "score": np.take(pred, res),
            }
        ).sort_values("score", ascending=False)
        return r


class EASE(BaseModel):
    def __init__(self, config):
        super(EASE, self).__init__()
        self.reg_weight = config["reg_weight"]

    def fit(self, X):
        # G = X.T.dot(X).toarray()
        G = X.T.dot(X)
        diagIndices = np.diag_indices(G.shape[0])
        G[diagIndices] += self.reg_weight
        P = np.linalg.inv(G)
        B = P / (-np.diag(P))
        B[diagIndices] = 0

        self.B = B
        self.pred = X.dot(B)


class AutoRec(nn.Module, BaseModel):
    def __init__(self, config):
        super(AutoRec, self).__init__()
        num_users = config["num_users"]
        num_items = config["num_items"]
        num_hidden = config["num_hidden"]
        dropout = config["dropout"]

        self.encoder = nn.Sequential(
            nn.Linear(num_items, num_hidden),
            # nn.Sigmoid(),  # 성능이 좋지 않음
            nn.ReLU(),
            nn.Dropout(dropout),
        )
        self.decoder = nn.Sequential(
            nn.Linear(num_hidden, num_items),
            # nn.Sigmoid(),  # 성능이 좋지 않음
            nn.ReLU(),
        )

    def forward(self, input: torch.Tensor) -> torch.Tensor:
        """
        input : __get__item(mat[item])  -> item 한 행씩 실행
        """
        enc_input = self.encoder(input)
        dec_input = self.decoder(enc_input)

        return dec_input
