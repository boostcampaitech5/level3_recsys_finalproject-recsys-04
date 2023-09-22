import re
import time
from datetime import datetime, timedelta
from .utils import OpenPyXL

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from typing import Union, Dict, List

class_dict = {
    "total_num_of_reviews": "_2pgHN-ntx6",  # 크롤링 할 element의 class
    "page_elements": "_1HJarNZHiI._2UJrM31-Ry",
    "next_button": "fAUKm1ewwo._2Ar8-aEUTq",
    "review_ul_parent": "_180GG7_7yx",
    "review_ul": "TsOLil1PRz",
    "user": "_3QDEeS6NLn",
    "coffee": "_14FigHP3K8",
    "satisfaction": "_1BgHSj04oF",
    "text_parent": "YEtwtZFLDz",
    "text": "_3QDEeS6NLn",
    "star_rating": "_15NU42F3kT",
}


def get_review_in_page(driver: webdriver) -> List[Dict[str, Union[str, int]]]:
    save_data = []
    wait = WebDriverWait(driver, 20)  # 특정 element를 완전히 로드하는데 최대 5초 기다림
    # scroll(driver)
    driver.execute_script(f"window.scrollTo({0}, {7000});")  # 리뷰 있는 곳까지 내리기
    time.sleep(2)

    # 최신순으로 정렬
    latest = driver.find_element(
        By.XPATH, '//*[@id="REVIEW"]/div/div[3]/div[1]/div[1]/ul/li[2]'
    )
    latest.click()  # 클릭
    time.sleep(1.5)

    # 총 리뷰 수
    review_count = 0
    stop: str = driver.find_element(
        By.CLASS_NAME, class_dict["total_num_of_reviews"]
    ).text
    stop: int = int(re.sub("[,]", "", stop))  # ',' 제거
    print(f"총 리뷰 수 : {stop}")

    # 페이지
    next_button = wait.until(
        EC.element_to_be_clickable((By.CLASS_NAME, class_dict["next_button"]))
    )

    now = datetime.now() - timedelta(days=1)
    today = ".".join(map(str, [now.year, now.month, now.day]))  # 현재 수집하고 있는 날짜

    format1 = "%Y.%m.%d"
    format2 = "%y.%m.%d."
    d1 = datetime.strptime(today, format1)

    ok = True  # 과거 데이터를 만나면 False

    while review_count < 20000:  # 최대 20000개까지 가능
        if not ok:  # 수집일보다 이전 데이터 리뷰를 만나면 종료(수집일에 해당하는 새로운 데이터만 수집)
            break
        time.sleep(1)  # 다음 페이지 로드 기다리기
        review_ul = wait.until(
            EC.element_to_be_clickable((By.CLASS_NAME, class_dict["review_ul_parent"]))
        ).find_element(By.CLASS_NAME, class_dict["review_ul"])

        for review in review_ul.find_elements(by=By.TAG_NAME, value="li"):
            review_count += 1
            try:
                date = review.find_element(
                    By.CSS_SELECTOR, "span._3QDEeS6NLn"
                ).text  # 리뷰를 남긴 날짜
                d2 = datetime.strptime(date, format2)

                # 데이터 수집 날짜와 리뷰를 남긴 날짜가 다를 경우 -> 수집 안함(매일 새롭게 쌓인 리뷰만 수집)
                if d1 != d2:
                    print(f"현재: {d1}, 리뷰 날짜: {d2}")
                    ok = False
                    break

                user = review.find_element(By.CLASS_NAME, class_dict["user"]).text
                coffee, grind = re.split(
                    "\s/\s",
                    review.find_element(By.CLASS_NAME, class_dict["coffee"]).text,
                )
                text = (
                    review.find_element(By.CLASS_NAME, class_dict["text_parent"])
                    .find_element(By.CLASS_NAME, class_dict["text"])
                    .text
                )
                star_rating = review.find_element(
                    By.CLASS_NAME, class_dict["star_rating"]
                ).text
                gram, coffee = ppcs_coffee(coffee)
                grind, satisfaction = ppcs_grind_and_get_satisfaction(grind)

                dict_data: Dict[str, Union[str, int]] = dict()
                dict_data["coffee"] = coffee
                dict_data["user"] = user
                dict_data["star_rating"] = star_rating
                dict_data["text"] = text
                dict_data["satisfaction"] = satisfaction
                dict_data["grind"] = grind
                dict_data["weight"] = gram
                dict_data["date"] = date

                save_data.append(dict_data)

            except:
                continue

        if review_count % 10000 == 0:  # 10000번마다 백업
            OpenPyXL.save_file(save_data)

        print(f"{review_count} / {stop}")
        next_button.click()  # 다음페이지 클릭

    return save_data


def ppcs_coffee(coffee: str) -> List[str, str]:
    """
    coffee에 대한 전처리
    ex) 1kg_블루드래곤어쩌구 -> ['1000g', '블루드래곤어쩌구']
    """
    coffee = coffee[6:]
    coffee = re.sub("1kg", "1000g", coffee)
    coffee = re.sub("(new)", "", coffee)
    coffee = re.sub("★ ", "", coffee)
    coffee = re.split("_", coffee)

    return coffee if len(coffee) == 2 else [None, coffee[0]]  # 예외 발생 가능


def ppcs_grind_and_get_satisfaction(grind: str) -> List[str, str]:
    """
    grind 정보와 맛 만족도를 한번에 가져옴, 이에 대한 전처리
    """
    grind = grind[7:]
    grind = re.sub("[0-9][.]\s?", "", grind)
    grind, satisfaction = re.split(
        "[\r\n|\r|\n]", grind
    )  # '\n'을 기준으로 grind정보와 맛 만족도 문단 구분
    satisfaction = re.sub("\s", "", satisfaction)
    satisfaction = re.split("맛만족도", satisfaction)[1][:4]

    return grind, satisfaction
