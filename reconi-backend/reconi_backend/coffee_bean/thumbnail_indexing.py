import os
from .models import CoffeeBean


def index_images():
    for instance in CoffeeBean.objects.all():
        image_filename = str(instance.id) + ".png"  # 파일 확장자가 .png인 경우로 가정합니다.

        # roastery 값을 가져옵니다.
        roastery = instance.roastery

        # roastery 값이 ('콩스콩스', '레스트빈', '커피창고', '라인코 원두커피', '베러베스트')에 포함되지 않는 경우에만 인덱싱을 진행합니다.
        if roastery in ("콩스콩스", "레스트빈", "커피창고", "라인코 원두커피", "베러베스트"):
            continue

        media_path = "/Users/woo/reconi-backend/reconi_backend/media"
        # media_path = "/Users/woo/reconi-backend/reconi_backend/media"

        if os.path.exists(
            os.path.join(media_path, "thumbnails/", image_filename)
        ):
            # 저장 경로를 './media/thumbnails'로 변경합니다.
            image_path = os.path.join("thumbnails/", image_filename)
            instance.thumbnail = image_path
            instance.save()


def index_representative_thumbnail():
    roasteries = ("콩스콩스", "레스트빈", "커피창고", "라인코 원두커피", "베러베스트")

    for index, roastery in enumerate(roasteries):
        # 대표 썸네일 파일명을 가져옵니다. 'thumbnails' 디렉토리에 파일명이 0.png, 1.png, 2.png, ... 와 같이 순서대로 되어 있다고 가정합니다.
        representative_thumbnail_filename = os.path.join(
            "thumbnails/", f"{index}.png"
        )

        # 해당 로스터리의 모든 커피 원두들을 가져옵니다.
        coffee_beans = CoffeeBean.objects.filter(roastery=roastery)
        print(os.path.join("media", representative_thumbnail_filename))
        # 해당 로스터리의 모든 커피 원두들에 대해 대표 썸네일 파일을 인덱싱합니다.
        for coffee_bean in coffee_beans:
            # 대표 썸네일 파일이 존재할 경우 이미지 필드를 인덱싱합니다.
            if os.path.exists(
                os.path.join("media", representative_thumbnail_filename)
            ):
                coffee_bean.thumbnail = representative_thumbnail_filename
                coffee_bean.save()
