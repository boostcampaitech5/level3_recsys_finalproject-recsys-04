import urllib.request
import pandas as pd


def download_with_urllib(url: str, output_file: str, save_path: str):
    """
    url: 이미지 링크
    output_file: 저장할 파일 이름(ex. '129.png')
    save_path: 저장할 경로(ex.'./downloads')
    """

    try:
        urllib.request.urlretrieve(url, f"{save_path}/{output_file}")
        print(f"다운로드 완료: {save_path}/{output_file}")
    except Exception as e:
        print(f"다운로드 실패: {e}")


coffee = pd.read_csv(
    "/Users/woo/reconi-backend/reconi_backend/thumbnails.csv"
)  # 공장형 원두를 제외한 로스터리들은 각각 썸네일 이미지링크를 가지고 있음


save_path = "./media/thumbnails"  # 저장경로 변경해서 사용
for i in range(len(coffee)):
    bean_id = coffee.iloc[i]["id"]
    link = coffee.iloc[i]["thumbnail_link"]
    if not link:
        continue

    download_with_urllib(link, f"{bean_id}.png", save_path)
