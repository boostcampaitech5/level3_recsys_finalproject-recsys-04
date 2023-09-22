import time
from datetime import datetime
import os
import pandas as pd
from typing import Union, Dict, List

from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager


def get_driver(user_agent: str) -> webdriver:
    options = ChromeOptions()
    options.add_argument("user-agent=" + user_agent)
    options.add_argument("lang=ko_KR")
    options.add_argument("headless")  # chrome 안띄움
    options.add_argument("disable-gpu")
    options.add_argument("--no-sandbox")
    # chrome 드라이버 자동 설치
    driver = webdriver.Chrome(
        service=ChromeService(ChromeDriverManager().install()), options=options
    )
    return driver


def get_file_name() -> str:
    time_str = time.strftime("%Y%m%d-%H%M%S")
    return time_str + ".csv"


class OpenPyXL:
    @staticmethod
    def save_file(save_data: List[List[Dict[str, Union[str, int]]]]) -> None:
        # 크롤링 결과
        results = pd.DataFrame(save_data)
        results = results.rename(
            columns={
                "coffee": "상품명",
                "user": "구매자 이름",
                "star_rating": "구매자 평점",
                "text": "리뷰 내용",
                "satisfaction": "맛 만족도",
            }
        )

        file_name = get_file_name()
        save_dir = "/opt/ml/coffee/dataset/raw_data/reviews/naver"
        os.makedirs(save_dir, exist_ok=True)  # 디렉토리 생성

        results.to_csv(os.path.join(save_dir, file_name), index=False)

        now = datetime.now()
        print(f"{now} 데이터 Done!")
