import itertools
import time
import numpy as np
import pandas as pd
from tqdm import tqdm

from data import load_table


class Evaluator:
    def __init__(self, config, predictor, item_profile):
        self.config = config
        self.item_profile = item_profile
        self.predictor = predictor
        self.topk = self.predictor.topk

        # -- 유저 인풋
        self.user_inputs = (
            self.make_n_user_inputs()
        )  # 위 모든 유저에 대해 계산 시 시간이 오래 걸리므로 일부만 추출

        # -- 유저 인풋에 따른 예측 결과
        self.preds = self.predict()

    def make_n_user_inputs(self):
        np.random.seed(self.config["seed"])

        # 11개 클래스로 이루어진 다항분포의 확률을 정규분포처럼 분배하는 함수
        def generate_probabilities():
            # 정규분포의 평균과 표준편차 설정
            mean = 0.5
            std_dev = 0.15

            # 정규분포로부터 랜덤한 확률 값을 생성
            probabilities = np.random.normal(loc=mean, scale=std_dev, size=11)

            # 생성된 확률 값들이 0과 1 사이에 있도록 조정 (확률은 합이 1이어야 함)
            probabilities = np.clip(probabilities, 0, 1)

            # 생성된 확률 값을 합이 1이 되도록 정규화
            probabilities /= probabilities.sum()

            return probabilities

        num_classes = 11  # 0부터 10까지
        num_samples = self.config["test_size"]

        # 설문조사에 의거한 확률 (0점은 이상치라고 가정하고 제외)
        acidity_probabilities = [
            0,
            0.157,
            0.157,
            0.1825,
            0.1825,
            0.095,
            0.095,
            0.0585,
            0.0585,
            0.0075,
            0.0075,
        ]
        sweetness_probabilities = [
            0,
            0.0585,
            0.0585,
            0.1105,
            0.1105,
            0.156,
            0.156,
            0.1495,
            0.1495,
            0.026,
            0.026,
        ]
        body_probabilities = [
            0,
            0.014,
            0.014,
            0.052,
            0.052,
            0.179,
            0.179,
            0.2215,
            0.2215,
            0.033,
            0.033,
        ]

        # 설문조사에 없으므로 정규분포에서 추출
        aroma_probabilities = generate_probabilities()
        roasting_point_probabilities = generate_probabilities()

        acidity_samples = np.random.multinomial(
            1, acidity_probabilities, size=num_samples
        )
        sweetness_samples = np.random.multinomial(
            1, sweetness_probabilities, size=num_samples
        )
        body_samples = np.random.multinomial(
            1, body_probabilities, size=num_samples
        )

        aroma_samples = np.random.multinomial(
            1, aroma_probabilities, size=num_samples
        )
        roasting_point_samples = np.random.multinomial(
            1, roasting_point_probabilities, size=num_samples
        )

        result = {
            "aroma": [],
            "acidity": [],
            "sweetness": [],
            "body": [],
            "roasting_point": [],
        }
        acidity_result = np.where(acidity_samples == True)[1]
        sweetness_result = np.where(sweetness_samples == True)[1]
        body_result = np.where(body_samples == True)[1]
        aroma_result = np.where(aroma_samples == True)[1]
        roasting_point_result = np.where(roasting_point_samples == True)[1]

        for acid, sweet, body, aroma, roasting_point in zip(
            acidity_result,
            sweetness_result,
            body_result,
            aroma_result,
            roasting_point_result,
        ):
            result["aroma"].append(aroma)
            result["acidity"].append(acid)
            result["sweetness"].append(sweet)
            result["body"].append(body)
            result["roasting_point"].append(roasting_point)

        user_inputs = np.array(pd.DataFrame(result))

        return user_inputs

    def predict(self):
        predictor = self.predictor
        predictor.user_preferences = self.user_inputs

        preds = predictor.recommend_for_target_user()
        return preds

    def get_euclidean_distance(self):
        item_profile = self.item_profile
        user_inputs = self.user_inputs
        preds = self.preds

        # 모든 유저의 유클리디안 거리를 담을 리스트
        euclidean_distance_list = []

        # topk 아이템들의 프로파일 정보를 한 번에 추출하여 저장
        topk_items = [
            item_profile[item_profile["id"].isin(preds[i])]
            .drop("id", axis=1)
            .values
            for i in range(len(preds))
        ]

        # 각 유저 인풋별로 예측값과 유클리디안 거리 측정
        for user_input in tqdm(
            user_inputs, desc="Calculating distance"
        ):  # input 수만큼 반복
            # 유저 선호 정보와, 예측된 아이템 프로파일 정보 간 거리 계산 (벡터화)
            distances = np.linalg.norm(topk_items - user_input, axis=2)
            euclidean_distance_list.extend(distances.ravel().tolist())

        return np.mean(euclidean_distance_list)

    def get_entropy_diversity(self):  # 유저 인풋 크기가 100인 경우 1초 미만, 1000인 경우 1분 소요
        preds = self.preds  # 각 유저 인풋마다 예측된 결과가 담긴 리스트

        entropy_list = []
        for pred_items in preds:
            # Count the occurrences of each item in the list
            item_counts = {}
            for item in pred_items:
                item_counts[item] = item_counts.get(item, 0) + 1

            # Calculate the probability of each item
            total_count = len(pred_items)
            item_probabilities = [
                count / total_count for count in item_counts.values()
            ]

            # Calculate the entropy diversity
            entropy_diversity = -np.sum(
                p * np.log2(p) for p in item_probabilities
            )
            entropy_list.append(entropy_diversity)

        return np.mean(entropy_list)

    def get_diversity(self):
        item_profile = self.item_profile
        preds = self.preds

        all_pred_items = []
        for pred_items in preds:
            for item in pred_items:
                all_pred_items.append(item)

        unique_pred_items = np.unique(all_pred_items)

        # 전체 아이템 중, 예측된 고유 아이템의 비율
        return len(unique_pred_items) / len(item_profile)
