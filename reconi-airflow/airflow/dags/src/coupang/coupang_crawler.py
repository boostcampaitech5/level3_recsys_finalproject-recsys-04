from bs4 import BeautifulSoup as bs
from typing import Optional, Union, Dict, List

import time
from datetime import datetime, timedelta

import os
import re
import requests as rq
import json
import pandas as pd

import logging

# 로거 인스턴스 생성
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# 콘솔 핸들러 생성
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

# 로그 포맷 설정
log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
formatter = logging.Formatter(log_format)
console_handler.setFormatter(formatter)

# 콘솔 핸들러를 로거에 추가
logger.addHandler(console_handler)


def get_headers(
    key: str, default_value: Optional[str] = None
) -> Dict[str, Dict[str, str]]:
    """Get Headers"""
    JSON_FILE: str = "/opt/ml/coffee/airflow/dags/json/headers.json"

    with open(JSON_FILE, "r", encoding="UTF-8") as file:
        headers: Dict[str, Dict[str, str]] = json.loads(file.read())

    try:
        return headers[key]
    except Exception:
        if default_value:
            return default_value
        raise EnvironmentError(f"Set the {key}")


class Coupang:
    @staticmethod
    def get_product_code(url: str) -> str:
        """입력받은 URL 주소의 PRODUCT CODE 추출하는 메소드"""
        prod_code: str = url.split("products/")[-1].split("?")[0]
        return prod_code

    def __init__(self, url, save_none_contents: bool) -> None:
        self.__headers: Dict[str, str] = get_headers(key="headers")
        self.url = url
        self.save_none_contents = save_none_contents
        self.flag = False

    def main(self) -> List[List[Dict[str, Union[str, int]]]]:
        # URL 주소
        URL: str = self.url

        # URL의 Product Code 추출
        prod_code: str = self.get_product_code(url=URL)

        # __headers에 referer 키 추가
        self.__headers["referer"] = URL

        session = rq.Session()

        # 평점별 리뷰 개수
        # URL 주소 재가공
        URLS: List[str] = [
            f"https://www.coupang.com/vp/product/reviews?productId={prod_code}&page={page}&size=5&sortBy=DATE_DESC&ratings=&q=&viRoleCode=3&ratingSummary=true"
            for page in range(1, 1500 + 1)  # 리뷰는 최대 1페이지에 5개씩 300페이지까지 총 1500개 확인 가능, 최신순으로 정렬
        ]

        saved_data_list = []
        for url in URLS:  # 1페이지부터 1500페이지까지의 링크 순회
            if self.flag:  # 수집일자에 해당하는 데이터만 수집함(더 이상 다음 페이지 리뷰 확인할 필요없음)
                break
            saved_data = self.fetch(
                url=url,
                session=session,
                save_none_contents=self.save_none_contents,
            )

            if saved_data is None:  # 리뷰가 더 이상 없으므로 데이터를 더 이상 수집하지 않아도 됨
                break
            else: # 리뷰가 있는 경우, 수집한 데이터 추가
                saved_data_list.append(saved_data)

        return saved_data_list

    def fetch(
        self, url: str, session, save_none_contents: bool = False
    ) -> List[Dict[str, Union[str, int]]]:
        save_data: List[Dict[str, Union[str, int]]] = list()

        now = datetime.now() - timedelta(days=1)
        today = ".".join(map(str, [now.year, now.month, now.day]))

        with session.get(url=url, headers=self.__headers) as response:
            html = response.text
            soup = bs(html, "html.parser")

            # Article Boxes
            # 해당 페이지에서의 리뷰 개수
            article_lenth = len(soup.select("article.sdp-review__article__list"))

            # 리뷰가 없으면 조기 종료하기 위함
            if article_lenth == 0:
                return

            for idx in range(article_lenth):
                dict_data: Dict[str, Union[str, int]] = dict()
                articles = soup.select("article.sdp-review__article__list")

                # 날짜
                date = articles[idx].select_one(
                    "div.sdp-review__article__list__info__product-info__reg-date"
                )
                if date is None or date.text == "":
                    date = "알 수 없음"
                else:
                    date = date.text.strip()

                # 데이터를 수집하는 날짜와 일치하는 데이터만 수집함
                if date != today:
                    logger.info(f"데이터 수집일: {today}, 리뷰 작성일: {date}")
                    self.flag = True
                    return save_data  # 더 이상 해당 페이지 데이터 확인할 필요 없음

                # 리뷰 내용
                review_content = articles[idx].select_one(
                    "div.sdp-review__article__list__review > div"
                )
                if review_content is None:
                    if save_none_contents:  # 리뷰 내용이 없어도 해당 리뷰를 저장
                        review_content = "등록된 리뷰내용이 없습니다"
                    else:  # 리뷰 내용이 없으면 해당 리뷰는 패스
                        continue
                else:
                    review_content = re.sub("[\n\t]", "", review_content.text.strip())

                # 구매자 이름
                user_name = articles[idx].select_one(
                    "span.sdp-review__article__list__info__user__name"
                )
                if user_name is None or user_name.text == "":
                    user_name = "-"
                else:
                    user_name = user_name.text.strip()

                # 평점
                rating = articles[idx].select_one(
                    "div.sdp-review__article__list__info__product-info__star-orange"
                )
                if rating is None:
                    rating = 0
                else:
                    rating = int(rating.attrs["data-rating"])

                # 구매자 상품명
                prod_name = articles[idx].select_one(
                    "div.sdp-review__article__list__info__product-info__name"
                )
                if prod_name is None or prod_name.text == "":
                    prod_name = "-"
                else:
                    prod_name = prod_name.text.strip()

                # 헤드라인(타이틀)
                headline = articles[idx].select_one(
                    "div.sdp-review__article__list__headline"
                )
                if headline is None or headline.text == "":
                    headline = "등록된 헤드라인이 없습니다"
                else:
                    headline = headline.text.strip()

                # 맛 만족도
                answer = articles[idx].select_one(
                    "span.sdp-review__article__list__survey__row__answer"
                )
                if answer is None or answer.text == "":
                    answer = "맛 평가 없음"
                else:
                    answer = answer.text.strip()

                dict_data["상품명"] = prod_name
                dict_data["구매자 이름"] = user_name
                dict_data["구매자 평점"] = rating
                dict_data["리뷰 제목"] = headline
                dict_data["리뷰 내용"] = review_content
                dict_data["맛 만족도"] = answer
                dict_data["날짜"] = date
                dict_data["플랫폼"] = "쿠팡"

                save_data.append(dict_data)


            time.sleep(1)

            return save_data


class OpenPyXL:
    @staticmethod
    def save_file(
        title: str, roastery: str, url: str, save_none_contents: bool
    ) -> None:
        # 크롤링 결과
        results: List[List[Dict[str, Union[str, int]]]] = Coupang(
            url=url, save_none_contents=save_none_contents
        ).main()

        all_empty = all(not result for result in results)
        if all_empty:  # 저장된 리뷰가 없으면 파일을 저장하지 않음
            logger.info(f"{title}의 새로운 리뷰가 없습니다.")
            return

        # 파일명이 있는 리뷰의 위치
        name_loc = 0
        for i, result in enumerate(results):
            if len(result) != 0:
                name_loc = i
                break

        data = []
        for x in results:
            for result in x:
                data.append(result)

        result_df = pd.DataFrame(data)

        raw_review_dataset_path = "/opt/ml/coffee/dataset/raw_data/reviews/"
        savePath: str = raw_review_dataset_path + "coupang"
        fileName: str = results[name_loc][0]["상품명"] + ".csv"

        if not os.path.exists(savePath):
            os.mkdir(savePath)

        result_df["원두이름"] = title
        result_df["로스터리"] = roastery
        result_df["날짜"] = pd.to_datetime(result_df["날짜"]).dt.strftime(
            "%Y-%m-%d %H:%M:%S %Z"
        )

        result_df.to_csv(os.path.join(savePath, fileName), index=False)

        logger.info(f"파일 저장 완료!\n\n{os.path.join(savePath, fileName)}")
