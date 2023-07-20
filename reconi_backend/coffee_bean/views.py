from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

import random
from .filters import filter_parameters

# Import Models
from .models import (
    CoffeeBeanOrigin,
    CoffeeBean,
    CoffeeBeanOrigins,
    CoffeeBeanReview,
    CoffeeInCart,
)

# Import Serializers
from .serializers import (
    CoffeeBeanSerializer,
    CoffeeBeanOriginSerializer,
    CoffeeBeanOriginsSerializer,
    CoffeeBeanReviewSerializer,
    CoffeeInCartSerializer,
)


class CoffeeBeanPagination(PageNumberPagination):
    page_size = 30
    page_size_query_param = "page_size"
    max_page_size = 30


######################### V1 #########################


class CoffeeBeanOriginViewSet(viewsets.ModelViewSet):
    queryset = CoffeeBeanOrigin.objects.all()
    serializer_class = CoffeeBeanOriginSerializer


class CoffeeBeanViewSet(viewsets.ModelViewSet):
    queryset = CoffeeBean.objects.all()
    serializer_class = CoffeeBeanSerializer
    pagination_class = CoffeeBeanPagination

    # 필터링 로직을 함수로 분리합니다.
    def apply_filters(self, queryset, filters):
        for field_name, param_name in filters.items():
            param_value = self.request.query_params.get(param_name)
            if param_value is not None:
                if "__" in param_name:
                    param_lookup = param_name.split("__")[1]  # gte, lte 등
                    filter_params = {
                        f"{field_name}__{param_lookup}": param_value
                    }
                else:
                    filter_params = {f"{field_name}__exact": param_value}

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
    def category_filtered(self, request):
        # 필터를 적용할 queryset
        queryset = CoffeeBean.objects.all()

        # 원산지 필터를 적용하는 경우:
        origins = request.query_params.getlist("origins_country")
        if origins:
            queryset = queryset.filter(
                coffeebeanorigins__origin__country__in=origins
            )

        # 추가적인 필터들을 적용합니다.
        filters = {
            "aroma": "aroma__exact",
            "acidity": "acidity",
            "sweetness": "sweetness",
            "body": "body",
            "balance": "balance",
            "roasting_point": "roasting_point",
            "roastery": "roastery__exact",
        }

        queryset = self.apply_filters(queryset, filters)

        # Serializer를 통해 직렬화한 후 응답합니다.
        serializer = CoffeeBeanSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def paginated_list(self, request):
        # 페이지네이션을 적용한 전체 커피 원두 아이템을 가져옵니다.
        paginated_coffee_beans = self.paginate_queryset(self.queryset)

        # 가져온 페이지네이션 된 커피 원두 아이템을 Serializer를 통해 직렬화한 후 응답합니다.
        serializer = CoffeeBeanSerializer(paginated_coffee_beans, many=True)
        return self.get_paginated_response(serializer.data)

    @action(detail=False, methods=["get"])
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
    def recommended(self, request):
        user = request.user
        # 전체 커피 원두 아이템을 가져옵니다.
        all_coffee_beans = CoffeeBean.objects.all()
        # 커피 원두 아이템을 랜덤하게 3개 선택합니다.
        random_coffee_beans = random.sample(list(all_coffee_beans), 3)
        # 선택된 커피 원두 아이템을 Serializer를 통해 직렬화한 후 응답합니다.
        serializer = CoffeeBeanSerializer(random_coffee_beans, many=True)
        return Response(serializer.data)


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
