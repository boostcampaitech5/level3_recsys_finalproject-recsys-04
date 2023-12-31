from rest_framework.permissions import AllowAny
from rest_framework import viewsets
from rest_framework.decorators import action, permission_classes
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

import random
import requests
from .filters import filter_parameters
from user.serializers import ReconiUserSerializer

from django.db.models import Q
from django.conf import settings
from django.shortcuts import get_object_or_404

# Import Models
from .models import (
    CoffeeBeanOrigin,
    CoffeeBean,
    CoffeeBeanOrigins,
    CoffeeBeanReview,
    CoffeeInCart,
    RecommendedCoffeeColdStart,
    RecommendedCoffeeNotColdStart,
)

# Import Serializers
from .serializers import (
    CoffeeBeanSerializer,
    CoffeeBeanOriginSerializer,
    CoffeeBeanOriginsSerializer,
    CoffeeBeanReviewSerializer,
    CoffeeInCartSerializer,
    RecommendedCoffeeNotColdStartSerializer,
)
from django.contrib.auth import get_user_model

TIMEOUT_SECONDS = 10
ReconiUser = get_user_model()


class CoffeeBeanPagination(PageNumberPagination):
    page_size = 30
    page_size_query_param = "page_size"
    max_page_size = 30


######################### V1 #########################


class CoffeeBeanOriginViewSet(viewsets.ModelViewSet):
    queryset = CoffeeBeanOrigin.objects.all()
    serializer_class = CoffeeBeanOriginSerializer


def add_recommendations_from_predictions(model, predictions, user):
    # '주어진 추천 결과 저장' 테이블에 유저와 커피 원두 아이템을 추가
    user = get_object_or_404(ReconiUser, id=user)
    rec_coffee, _ = model.objects.get_or_create(user=user)

    rec_coffee.coffee_beans.clear()
    for coffee_pk in predictions:
        coffee_item = get_object_or_404(CoffeeBean, pk=coffee_pk)
        rec_coffee.coffee_beans.add(coffee_item)

    # 'RecommendationsCoffeeColdStart' 객체를 저장
    rec_coffee.save()


class CoffeeBeanViewSet(viewsets.ModelViewSet):
    queryset = CoffeeBean.objects.all()
    serializer_class = CoffeeBeanSerializer
    pagination_class = CoffeeBeanPagination

    # 필터링 로직을 함수로 분리합니다.
    def apply_filters(self,request, queryset, filters):
        for field_name, param_name in filters.items():
            param_value = request.query_params.get(param_name)
            print(field_name, param_name,param_value)
            if param_value is not None:
                if "__" in param_name:
                    filter_params = {
                        f"{param_name}": param_value
                    }
                else:
                    filter_params = {f"{field_name}__exact": param_value}
                print(filter_params)
                queryset = queryset.filter(**filter_params)

        return queryset

    @swagger_auto_schema(
        method="get",
        manual_parameters=[
            openapi.Parameter(
                name, openapi.IN_QUERY, type=param_type, description=description
            )
            for name, description, param_type in filter_parameters
        ],
    )
    @action(detail=False, methods=["get"])
    @permission_classes([AllowAny])
    def category_filtered(self, request):
        # 필터를 적용할 queryset
        queryset = CoffeeBean.objects.all()

        # 원산지 필터를 적용하는 경우:
        origins = request.query_params.get("origins_country")
        if origins:
            origins = origins.split(',')
            print(origins)
            queryset = queryset.filter(
                coffeebeanorigins__origin__country__in=origins
            )
        # 로스터리 필터를 적용하는 경우:
        roastery = request.query_params.get("roastery")
        if roastery:
            roastery = roastery.split(',')
            print(origins)
            queryset = queryset.filter(
                            roastery__in=roastery
                        )
            
        # 추가적인 필터들을 적용합니다.
        filters = {
            "acidity__lte": "acidity__lte",
            "acidity__gte": "acidity__gte",
            "sweetness__lte": "sweetness__lte",
            "sweetness__gte": "sweetness__gte",
            "body__lte": "body__lte",
            "body__gte": "body__gte",
            "roasting_point__lte": "roasting_point__lte",
            "roasting_point__gte": "roasting_point__gte",
        }

        queryset = self.apply_filters(request,queryset, filters)

        # Serializer를 통해 직렬화한 후 응답합니다.
        serializer = CoffeeBeanSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    @permission_classes([AllowAny])
    def paginated_list(self, request):
        # 페이지네이션을 적용한 전체 커피 원두 아이템을 가져옵니다.
        paginated_coffee_beans = self.paginate_queryset(self.queryset)

        # 가져온 페이지네이션 된 커피 원두 아이템을 Serializer를 통해 직렬화한 후 응답합니다.
        serializer = CoffeeBeanSerializer(paginated_coffee_beans, many=True)
        return self.get_paginated_response(serializer.data)

    @action(detail=False, methods=["get"])
    @permission_classes([AllowAny])
    def random_items(self, request):
        # 전체 커피 원두 아이템을 가져옵니다.
        all_coffee_beans = CoffeeBean.objects.all()

        # 커피 원두 아이템을 랜덤하게 20개 선택합니다.
        random_coffee_beans = random.sample(list(all_coffee_beans), 20)

        # random_coffee_beans = CoffeeBean.objects.order_by("?")[:20]
        # 선택된 커피 원두 아이템을 Serializer를 통해 직렬화한 후 응답합니다.
        serializer = CoffeeBeanSerializer(random_coffee_beans, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    @permission_classes([AllowAny])
    def all_items(self, request):
        # 전체 커피 원두 아이템을 가져옵니다.
        all_coffee_beans = CoffeeBean.objects.all()

        # random_coffee_beans = CoffeeBean.objects.order_by("?")[:20]
        # 선택된 커피 원두 아이템을 Serializer를 통해 직렬화한 후 응답합니다.
        serializer = CoffeeBeanSerializer(all_coffee_beans, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    @permission_classes([AllowAny])
    def unique_categories(self, request):
        # 중복 제거된 모든 roastery 값을 가져옵니다.
        unique_roastery_values = (
            CoffeeBean.objects.order_by()
            .values_list("roastery", flat=True)
            .distinct()
        )
        # 중복 제거된 모든 원산지 값을 가져옵니다.
        unique_origin_values = (
            CoffeeBeanOrigins.objects.order_by()
            .values_list("origin__country", flat=True)
            .distinct()
        )
        # roastery와 원산지 값을 각각 딕셔너리에 추가하여 합쳐서 응답합니다.
        unique_categories = {
            "roastery": list(unique_roastery_values),
            "origin": list(unique_origin_values),
        }
        return Response(unique_categories)

    @action(detail=False, methods=["get"])
    def decaffeinated_coffee_beans(self, request):
        # 제목에 '디카페인'이 포함된 데이터를 조회합니다.
        queryset = CoffeeBean.objects.filter(title__icontains="디카페인")

        # Serializer를 통해 직렬화한 후 응답합니다.
        serializer = CoffeeBeanSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["post"])
    def cold_start_recommended(self, request):
        user = request.user
        data = request.data
        inference_server_url = getattr(settings, "INFERENCE_COLDSTART", "")

        #### 제출된 Form과 ReconiUserSerializer 기반으로 유저 정보 업데이트
        user_serializers = ReconiUserSerializer(user, data=data, partial=True)
        if user_serializers.is_valid():
            user_serializers.save()
        else:
            Response(user_serializers.errors, status=400)

        #### JSON 데이터에서 필요한 정보 추출
        #### Inference Server에 전달할 데이터 형식에 맞게 Payload를 가공합니다.
        payload = {
            "dataframe_records": [
                {
                    "aroma": data.get("aroma"),
                    "acidity": data.get("acidity"),
                    "sweetness": data.get("sweetness"),
                    "body_feel": data.get("body_feel"),
                    "roasting_characteristics": data.get(
                        "roasting_characteristics"
                    ),
                }
            ]
        }

        ##### Inference Server에 POST 요청을 보냅니다.

        try:
            response = requests.post(
                inference_server_url, json=payload, timeout=TIMEOUT_SECONDS
            )
            predictions = response.json()["predictions"]
            # {"predictions" : [1,2,3]}

            # Inference 결과 DB 인덱싱
            add_recommendations_from_predictions(
                RecommendedCoffeeColdStart, predictions, user.id
            )

        except requests.exceptions.RequestException:
            # 요청이 실패한 경우 에러 메시지를 DRF의 응답으로 반환합니다.
            # print(response)
            return Response(
                {"error": "Failed to send inference request."}, status=500
            )

        # 추천된 커피 원두 데이터를 Top 3개만 가져옵니다.
        recommended_coffee_item_ids = RecommendedCoffeeColdStart.objects.get(
            user=user
        ).coffee_beans.values_list("id", flat=True)

        # 선택된 커피 원두 아이템을 Serializer를 통해 직렬화한 후 응답합니다.
        coffee_beans = CoffeeBean.objects.filter(
            id__in=recommended_coffee_item_ids
        ).order_by('id')

        serializer = CoffeeBeanSerializer(coffee_beans, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def not_cold_start_recommended(self, request):
        user = request.user
        inference_server_url = getattr(settings, "INFERENCE_NOTCOLDSTART", "")
        cart_data = CoffeeInCart.objects.filter(user=user.id).values_list(
            "user_id", "coffee_beans__id"
        )

        #### JSON 데이터에서 필요한 정보 추출
        #### Inference Server에 전달할 데이터 형식에 맞게 Payload를 가공합니다.
        payload = {"dataframe_records": []}

        # 가져온 데이터를 딕셔너리로 구성합니다.
        for user_id, coffee_id in cart_data:
            if user_id not in payload["dataframe_records"]:
                payload["dataframe_records"].append(
                    {"user": str(user_id), "item": coffee_id, "rating": 1}
                )
        ##### Inference Server에 POST 요청을 보냅니다.
        try:
            response = requests.post(
                inference_server_url, json=payload, timeout=TIMEOUT_SECONDS
            )
            predictions = response.json()["predictions"]
            # {"predictions" : [1,2,3]}

            # Inference 결과 DB 인덱싱
            # bulk를 통한 일괄 데이터 업데이트가 필요해보임 -> 응답시간을 줄이기 위해서
            for user, prediction in predictions.items():
                add_recommendations_from_predictions(
                    RecommendedCoffeeNotColdStart, prediction, user
                )

        except requests.exceptions.RequestException:
            # 요청이 실패한 경우 에러 메시지를 DRF의 응답으로 반환합니다.
            return Response(
                {"error": "Failed to send inference request."}, status=500
            )
        except KeyError:
            return Response(
                {"error": "No Cart For User"}, status=400
            )
        
        try:
            instance = RecommendedCoffeeNotColdStart.objects.get(user=user)

        except RecommendedCoffeeNotColdStart.DoesNotExist:
            return Response({"error": "User's Cart is Not Exist"}, status=404)

        # 추천된 커피 원두 데이터를 Top 3개만 가져옵니다.
        recommended_coffee_item_ids = instance.coffee_beans.values_list(
            "id", flat=True
        )

        # 선택된 커피 원두 아이템을 Serializer를 통해 직렬화한 후 응답합니다.
        coffee_beans = CoffeeBean.objects.filter(
            id__in=recommended_coffee_item_ids
        )

        serializer = CoffeeBeanSerializer(coffee_beans, many=True)
        return Response(serializer.data)

    # @action(detail=False, methods=["get"])
    # def not_cold_start_recommended(self, request):
    #     user = request.user

    #     try:
    #         instance = RecommendedCoffeeNotColdStart.objects.get(user=user)

    #     except RecommendedCoffeeNotColdStart.DoesNotExist:
    #         return Response({"error": "User's Cart is Not Exist"}, status=404)

    #     # 추천된 커피 원두 데이터를 Top 3개만 가져옵니다.
    #     recommended_coffee_item_ids = instance.coffee_beans.values_list(
    #         "id", flat=True
    #     )

    #     # 선택된 커피 원두 아이템을 Serializer를 통해 직렬화한 후 응답합니다.
    #     coffee_beans = CoffeeBean.objects.filter(
    #         id__in=recommended_coffee_item_ids
    #     )

    #     serializer = CoffeeBeanSerializer(coffee_beans, many=True)
    #     return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def user_cart_ids(self, request):
        user = request.user

        response = {}

        #### 담기 리스트
        try:
            coffeeincart = CoffeeInCart.objects.get(user=user)
            # 추천된 커피 원두 데이터를 Top 3개만 가져옵니다.
            coffeeincart_coffee_item_ids = (
                coffeeincart.coffee_beans.values_list("id", flat=True)
            )
            # 선택된 커피 원두 아이템을 Serializer를 통해 직렬화한 후 응답합니다.
            response["user_item_ids"] = list(coffeeincart_coffee_item_ids)
        except CoffeeInCart.DoesNotExist:
            response["user_item_ids"] = []

        return Response(response)

    @action(detail=False, methods=["get"])
    def mypage(self, request):
        user = request.user

        

        #### 담기 리스트
        try:
            coffeeincart = CoffeeInCart.objects.get(user=user)
            # 추천된 커피 원두 데이터를 Top 3개만 가져옵니다.
            coffeeincart_coffee_item_ids = (
                coffeeincart.coffee_beans.values_list("id", flat=True)
            )
            nickname = coffeeincart.user.nickname

            # 선택된 커피 원두 아이템을 Serializer를 통해 직렬화한 후 응답합니다.
            coffeeincart_coffee = CoffeeBean.objects.filter(
                id__in=coffeeincart_coffee_item_ids
            )

            cart = CoffeeBeanSerializer(coffeeincart_coffee, many=True).data

        except CoffeeInCart.DoesNotExist:
            cart = None

        #### Cold Start 추천 리스트
        try:
            recommendedcoffeecoldstart = RecommendedCoffeeColdStart.objects.get(
                user=user
            )
            # 추천된 커피 원두 데이터를 Top 3개만 가져옵니다.
            recommendedcoffeecoldstart_coffee_item_ids = (
                recommendedcoffeecoldstart.coffee_beans.values_list(
                    "id", flat=True
                )
            )

            # 선택된 커피 원두 아이템을 Serializer를 통해 직렬화한 후 응답합니다.
            recommendedcoffeecoldstart_coffee = CoffeeBean.objects.filter(
                id__in=recommendedcoffeecoldstart_coffee_item_ids
            )

            cold_start = CoffeeBeanSerializer(
                recommendedcoffeecoldstart_coffee, many=True
            ).data

        except RecommendedCoffeeColdStart.DoesNotExist:
            cold_start = None

        #### Not Cold Start 추천 리스트
        try:
            recommendedcoffeenotcoldstart = (
                RecommendedCoffeeNotColdStart.objects.get(user=user)
            )
            # 추천된 커피 원두 데이터를 Top 3개만 가져옵니다.
            recommendedcoffeenotcoldstart_coffee_item_ids = (
                recommendedcoffeenotcoldstart.coffee_beans.values_list(
                    "id", flat=True
                )
            )
            # 선택된 커피 원두 아이템을 Serializer를 통해 직렬화한 후 응답합니다.
            recommendedcoffeenotcoldstart_coffee = CoffeeBean.objects.filter(
                id__in=recommendedcoffeenotcoldstart_coffee_item_ids
            )

            not_cold_start = CoffeeBeanSerializer(
                recommendedcoffeenotcoldstart_coffee, many=True
            ).data
        except RecommendedCoffeeNotColdStart.DoesNotExist:
            not_cold_start = None

        # key vale 형식으로 데이터를 반환합니다.
        unique_categories = {
            "nickname" : nickname,
            "cart": cart,
            "not_cold_start": not_cold_start,
            "cold_start": cold_start,
        }
        return Response(unique_categories)


class CoffeeBeanOriginsViewSet(viewsets.ModelViewSet):
    queryset = CoffeeBeanOrigins.objects.all()
    serializer_class = CoffeeBeanOriginsSerializer


class CoffeeBeanReviewViewSet(viewsets.ModelViewSet):
    queryset = CoffeeBeanReview.objects.all()
    serializer_class = CoffeeBeanReviewSerializer


class CoffeeInCartViewSet(viewsets.ModelViewSet):
    queryset = CoffeeInCart.objects.all()
    serializer_class = CoffeeInCartSerializer

    @swagger_auto_schema(
        method="post",
        request_body=openapi.Schema(
            type="object",
            properties={
                "coffee_bean_id": openapi.Schema(
                    type="integer",
                    description="ID of the coffee bean to be added to the cart.",
                )
            },
        ),
    )
    @action(detail=False, methods=["post"])
    def add_to_cart(self, request):
        coffee_id = request.data.get("coffee_bean_id")  # 요청 데이터에서 coffee_id 추출
        user = request.user

        try:
            coffee_bean = CoffeeBean.objects.get(id=coffee_id)
        except CoffeeBean.DoesNotExist:
            return Response({"error": "Invalid coffee_id"}, status=400)

        cart, _ = CoffeeInCart.objects.get_or_create(user=user)

        cart.coffee_beans.add(coffee_bean)
        serializer = self.get_serializer(cart)
        return Response(serializer.data)

    @swagger_auto_schema(
        method="post",
        request_body=openapi.Schema(
            type="object",
            properties={
                "coffee_bean_id": openapi.Schema(
                    type="integer",
                    description="ID of the coffee bean to be removed from the cart.",
                )
            },
        ),
    )
    @action(detail=False, methods=["post"])
    def remove_from_cart(self, request):
        coffee_bean_id = request.data.get(
            "coffee_bean_id"
        )  # 요청 데이터에서 coffee_bean_id 추출
        user = request.user

        try:
            coffee_bean = CoffeeBean.objects.get(id=coffee_bean_id)
        except CoffeeBean.DoesNotExist:
            return Response({"error": "Invalid coffee_bean_id"}, status=400)

        try:
            cart = CoffeeInCart.objects.get(user=user)
        except CoffeeInCart.DoesNotExist:
            return Response({"error": "Cart is empty"}, status=400)

        cart.coffee_beans.remove(coffee_bean)  # ManyToManyField에서 커피를 제거합니다.

        serializer = self.get_serializer(cart)
        return Response(serializer.data)
