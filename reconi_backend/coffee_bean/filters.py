import django_filters
from .models import CoffeeBean
from drf_yasg import openapi

# 필터 파라미터들을 리스트로 정의합니다.
filter_parameters = [
    (
        "origins_country",
        "Comma-separated list of coffee bean origins (e.g., 에티오피아,콜롬비아)",
        openapi.TYPE_STRING,
    ),
    # ("aroma", "Coffee bean aroma", openapi.TYPE_NUMBER),
    # ("acidity", "Coffee bean acidity", openapi.TYPE_INTEGER),
    # ("sweetness", "Coffee bean sweetness", openapi.TYPE_INTEGER),
    # ("body", "Coffee bean body", openapi.TYPE_INTEGER),
    # ("balance", "Coffee bean balance", openapi.TYPE_NUMBER),
    # ("roasting_point", "Coffee bean roasting point", openapi.TYPE_NUMBER),
    ("roastery", "Coffee bean roastery", openapi.TYPE_STRING),
    ("aroma__gte", "Minimum value for coffee bean aroma", openapi.TYPE_NUMBER),
    ("aroma__lte", "Maximum value for coffee bean aroma", openapi.TYPE_NUMBER),
    (
        "acidity__gte",
        "Minimum value for coffee bean acidity",
        openapi.TYPE_INTEGER,
    ),
    (
        "acidity__lte",
        "Maximum value for coffee bean acidity",
        openapi.TYPE_INTEGER,
    ),
    (
        "sweetness__gte",
        "Minimum value for coffee bean sweetness",
        openapi.TYPE_INTEGER,
    ),
    (
        "sweetness__lte",
        "Maximum value for coffee bean sweetness",
        openapi.TYPE_INTEGER,
    ),
    ("body__gte", "Minimum value for coffee bean body", openapi.TYPE_INTEGER),
    ("body__lte", "Maximum value for coffee bean body", openapi.TYPE_INTEGER),
    (
        "balance__gte",
        "Minimum value for coffee bean balance",
        openapi.TYPE_NUMBER,
    ),
    (
        "balance__lte",
        "Maximum value for coffee bean balance",
        openapi.TYPE_NUMBER,
    ),
    (
        "roasting_point__gte",
        "Minimum value for coffee bean roasting point",
        openapi.TYPE_NUMBER,
    ),
    (
        "roasting_point__lte",
        "Maximum value for coffee bean roasting point",
        openapi.TYPE_NUMBER,
    ),
]


# class CoffeeBeanFilter(django_filters.FilterSet):
#     origin__country = django_filters.CharFilter(
#         field_name="coffeebeanorigins__origin__country", lookup_expr="exact"
#     )

#     class Meta:
#         model = CoffeeBean
#         fields = {
#             "aroma": ["exact", "gte", "lte"],
#             "acidity": ["exact", "gte", "lte"],
#             "sweetness": ["exact", "gte", "lte"],
#             "body": ["exact", "gte", "lte"],
#             "balance": ["exact", "gte", "lte"],
#             "roasting_point": ["exact", "gte", "lte"],
#             "roastery": ["exact"],
#         }
