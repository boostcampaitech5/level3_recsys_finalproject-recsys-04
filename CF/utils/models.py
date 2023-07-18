import numpy as np
import pandas as pd

from sklearn.preprocessing import LabelEncoder
from multiprocessing import Pool, cpu_count

from scipy.sparse import csr_matrix

import torch
import torch.nn as nn


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
        return df

    @staticmethod
    def predict_for_user(user, group, pred, items, k):
        watched = set(group["ci"])
        candidates = [item for item in items if item not in watched]
        pred = np.take(pred, candidates)
        # EASE 의 경우 모든 값이 0으로 예측되면 np.nan 발생
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
            # nn.Sigmoid(), # 성능이 좋지 않음
            nn.ReLU(),
            nn.Dropout(dropout),
        )
        self.decoder = nn.Sequential(
            nn.Linear(num_hidden, num_items),
            # nn.Sigmoid(), # 성능이 좋지 않음
            nn.ReLU(),
        )

    def forward(self, input: torch.Tensor) -> torch.Tensor:
        """
        input : __get__item(mat[item])  -> item 한 행씩 실행
        """
        enc_input = self.encoder(input)
        dec_input = self.decoder(enc_input)

        return dec_input
