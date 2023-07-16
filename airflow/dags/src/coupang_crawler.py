from bs4 import BeautifulSoup as bs
from typing import Optional, Union, Dict, List
import time
import os
import re
import requests as rq
import json
import pandas as pd


def get_headers(
    key: str, default_value: Optional[str] = None
) -> Dict[str, Dict[str, str]]:
    """Get Headers"""
    JSON_FILE: str = "json/headers.json"

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

    def main(self) -> List[List[Dict[str, Union[str, int]]]]:
        # URL 주소
        URL: str = self.url

        # URL의 Product Code 추출
        prod_code: str = self.get_product_code(url=URL)

        # __headers에 referer 키 추가
        self.__headers["referer"] = URL

        session = rq.Session()

        # 평점별 리뷰 개수
        with session.get(
            url=f"https://www.coupang.com/vp/product/reviews?productId={prod_code}&page=1&size=5&sortBy=ORDER_SCORE_ASC&ratings=&q=&viRoleCode=3&ratingSummary=true",
            headers=self.__headers,
        ) as response:
            html = response.text
            soup = bs(html, "html.parser")

            div_elements = soup.select(
                "div.sdp-review__article__list__hidden-rating > div.js_reviewArticleHiddenValue"
            )

            review_cnt_per_rating = [
                int(div_element["data-count"]) for div_element in div_elements
            ]  # 평점 5~1까지 순서대로 각 평점에서의 리뷰 개수 저장

            page_cnt_per_rating = map(
                lambda x: x // 5 + 1, review_cnt_per_rating
            )  # 리뷰 개수에 따라 페이지 수를 구함 (한 페이지 당 리뷰 5개)

        # URL 주소 재가공
        URLS: List[str] = [
            f"https://www.coupang.com/vp/product/reviews?productId={prod_code}&page={page}&size=5&sortBy=ORDER_SCORE_ASC&ratings={rating}&q=&viRoleCode=3&ratingSummary=true"
            for rating, page_cnt in zip(range(5, 0, -1), page_cnt_per_rating)
            for page in range(1, page_cnt + 1)
        ]

        saved_data_list = []
        for url in URLS:
            saved_data = self.fetch(
                url=url,
                session=session,
                save_none_contents=self.save_none_contents,
            )

            if saved_data is None:  # 리뷰가 더 이상 없으므로 데이터를 더 이상 수집하지 않아도 됨
                continue
            else:
                saved_data_list.append(saved_data)

        return saved_data_list

    def fetch(
        self, url: str, session, save_none_contents: bool = False
    ) -> List[Dict[str, Union[str, int]]]:
        save_data: List[Dict[str, Union[str, int]]] = list()

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
                if answer == None or answer.text == "":
                    answer = "맛 평가 없음"
                else:
                    answer = answer.text.strip()

                dict_data["상품명"] = prod_name
                dict_data["구매자 이름"] = user_name
                dict_data["구매자 평점"] = rating
                dict_data["리뷰 제목"] = headline
                dict_data["리뷰 내용"] = review_content
                dict_data["맛 만족도"] = answer

                save_data.append(dict_data)

                print(dict_data, "\n")

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
            print("리뷰가 없어 파일을 저장할 수 없습니다.")
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
        result_df.to_csv(os.path.join(savePath, fileName), index=False)

        print(f"파일 저장완료!\n\n{os.path.join(savePath,fileName)}")
