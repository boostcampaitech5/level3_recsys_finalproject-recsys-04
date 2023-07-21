import numpy as np

import torch
import torch.nn as nn
from torch.utils.data import Dataset

from tqdm.auto import tqdm

from itertools import product


class BaseTrainer:
    def __init__(self, model, train_set, test_set, logger):
        self.model = model
        self.train_set = train_set
        self.test_set = test_set

        self.logger = logger

    def ready_to_get_metrics(self) -> np.float32:
        # Get matrix from numpy Dataset
        self.test_mat = self.test_set.data
        self.test_mask = self.test_mat > 0

        # Get unseen users and items
        self.unseen_users = self.test_set.users - self.train_set.users
        self.unseen_items = self.test_set.items - self.train_set.items

    def masked_rmse(
        self,
        actual: torch.Tensor or np.ndarray,
        pred: torch.Tensor or np.ndarray,
        mask: torch.Tensor or np.ndarray,
    ) -> np.float32:
        mse = (((pred - actual) * mask) ** 2).sum() / mask.sum()

        if type(actual) is torch.Tensor:
            mse = mse.detach().cpu().numpy()

        return np.sqrt(mse)


class DeepLearningTrainer(BaseTrainer):
    def __init__(
        self,
        model,
        train_set,
        test_set,
        train_loader,
        test_loader,
        logger,
        config,
    ):
        super(DeepLearningTrainer, self).__init__(
            model, train_set, test_set, logger
        )

        self.train_loader = train_loader
        self.test_loader = test_loader

        self.epochs = config["epochs"]
        self.device = config["device"]
        self.loss_f = nn.MSELoss()
        self.optm = torch.optim.Adam(
            self.model.parameters(),
            lr=config["lr"],
            weight_decay=config["weight_decay"],
        )

    def run(self):
        best_epoch = 0
        best_rmse = np.inf

        for epoch in range(self.epochs):
            self.model.train()

            for input_vec in self.train_loader:
                input_mask = (input_vec > 0).cuda()
                input_vec = input_vec.float().cuda()

                self.model.zero_grad()
                reconstruction = self.model(input_vec)
                loss = self.loss_f(
                    reconstruction * input_mask, input_vec * input_mask
                )
                loss.backward()
                self.optm.step()

            self.model.eval()
            rmse = self.get_metrics()

            if epoch % 10 == 0:
                self.logger.info(f"|| [Epoch {epoch}] || RMSE: {rmse:.6f}")

            if rmse < best_rmse:
                best_rmse, best_epoch = rmse, epoch

        self.logger.info(
            f"|| Best epoch: {epoch} || Best_rmse: {best_rmse:.6f} || Best_epoch: {best_epoch}"
        )

        return self.model, best_rmse, best_epoch

    def get_metrics(self) -> np.float32:
        super().ready_to_get_metrics()

        self.test_mat = torch.Tensor(self.test_mat).cuda()
        self.test_mask = (self.test_mat > 0).cuda()

        # Reconstruct the test matrix
        reconstruction = self.model(self.test_mat)

        # Use a default rating of 3 for test users or
        # items without training observations.
        reconstruction = self.model(self.test_mat)
        for item, user in product(self.unseen_items, self.unseen_users):
            if self.test_mask[user, item]:
                reconstruction[user, item] = 3 / 5

        return self.masked_rmse(
            actual=self.test_mat, pred=reconstruction, mask=self.test_mask
        )


class ClosedFormTrainer(BaseTrainer):
    def __init__(self, model, train_set, test_set, logger, config):
        super(ClosedFormTrainer, self).__init__(
            model, train_set, test_set, logger
        )

    def run(self):
        self.model.fit(self.train_set.data)

        rmse = self.get_metrics()
        self.logger.info(f"|| Evaluation_RMSE: {rmse:.6f}")

        return self.model, rmse, 1

    def get_metrics(self) -> np.float32:
        super().ready_to_get_metrics()

        # Predict the test matrix
        # preds = self.test_mat.dot(self.model.B)
        preds = self.model.pred

        for item, user in product(self.unseen_items, self.unseen_users):
            if self.test_mask[user, item]:
                preds[user, item] = 3 / 5

        return self.masked_rmse(
            actual=self.test_mat, pred=preds, mask=self.test_mask
        )
