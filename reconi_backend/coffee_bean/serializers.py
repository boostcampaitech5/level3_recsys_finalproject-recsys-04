from rest_framework import serializers
from .models import (
    CoffeeBean,
    CoffeeBeanOrigin,
    CoffeeBeanReview,
    CoffeeBeanOrigins,
    CoffeeInCart,
)


class CoffeeBeanReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = CoffeeBeanReview
        fields = "__all__"


class CoffeeBeanOriginSerializer(serializers.ModelSerializer):
    class Meta:
        model = CoffeeBeanOrigin
        fields = "__all__"


class CoffeeBeanOriginsSerializer(serializers.ModelSerializer):
    origin = serializers.StringRelatedField()

    class Meta:
        model = CoffeeBeanOrigins
        fields = "__all__"


class CoffeeBeanSerializer(serializers.ModelSerializer):
    origins = serializers.StringRelatedField(
        many=True, source="coffeebeanorigins_set"
    )

    class Meta:
        model = CoffeeBean
        fields = "__all__"


class CoffeeInCartSerializer(serializers.ModelSerializer):
    coffee_beans = CoffeeBeanSerializer(many=True)

    class Meta:
        model = CoffeeInCart
        fields = "__all__"
