from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.core.validators import (
    MinValueValidator,
    MaxValueValidator,
)
from rest_framework.validators import UniqueValidator
from dj_rest_auth.registration.serializers import RegisterSerializer

from .models import SCENT_CHOICES, GENDER_CHOICES

ReconiUser = get_user_model()


class ReconiRegisterSerializer(RegisterSerializer):
    username = None
    nickname = serializers.CharField(max_length=50)
    gender = serializers.ChoiceField(
        choices=GENDER_CHOICES,
        allow_null=True,
        required=False,
    )
    age = serializers.IntegerField(allow_null=True, required=False)
    favorite_scent = serializers.ChoiceField(
        choices=SCENT_CHOICES,
        allow_null=True,
        required=False,
    )
    sweetness = serializers.FloatField(
        validators=[MinValueValidator(0), MaxValueValidator(10)],
        allow_null=True,
        required=False,
    )
    body_feel = serializers.FloatField(
        validators=[MinValueValidator(0), MaxValueValidator(10)],
        allow_null=True,
        required=False,
    )
    acidity = serializers.FloatField(
        validators=[MinValueValidator(0), MaxValueValidator(10)],
        allow_null=True,
        required=False,
    )
    roasting_characteristics = serializers.FloatField(
        validators=[MinValueValidator(0), MaxValueValidator(10)],
        allow_null=True,
        required=False,
    )

    def validate_nickname(self, value):
        """
        Check if the given nickname is unique during registration.
        """
        users = ReconiUser.objects.filter(nickname=value)
        if users.exists():
            raise serializers.ValidationError(
                "This nickname is already in use."
            )
        return value

    def validate_age(self, value):
        if value and (value < 0 or value > 120):
            raise ValidationError("Invalid age. Age must be between 0 and 120.")
        return value

    def get_cleaned_data(self):
        data = super().get_cleaned_data()
        # data = {}
        data["email"] = self.validated_data.get("email")
        data["nickname"] = self.validated_data.get("nickname")
        data["gender"] = self.validated_data.get("gender")
        data["age"] = self.validated_data.get("age")
        data["favorite_scent"] = self.validated_data.get("favorite_scent")
        data["sweetness"] = self.validated_data.get("sweetness")
        data["body_feel"] = self.validated_data.get("body_feel")
        data["acidity"] = self.validated_data.get("acidity")
        data["roasting_characteristics"] = self.validated_data.get(
            "roasting_characteristics"
        )
        return data


class ReconiUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReconiUser
        fields = (
            "email",
            "nickname",
            "gender",
            "age",
            "favorite_scent",
            "sweetness",
            "body_feel",
            "acidity",
            "roasting_characteristics",
            "password",
        )
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = ReconiUser(**validated_data)
        user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        instance.nickname = validated_data.get("nickname", instance.nickname)
        instance.gender = validated_data.get("gender", instance.gender)
        instance.age = validated_data.get("age", instance.age)
        instance.favorite_scent = validated_data.get(
            "favorite_scent", instance.favorite_scent
        )
        instance.sweetness = validated_data.get("sweetness", instance.sweetness)
        instance.body_feel = validated_data.get("body_feel", instance.body_feel)
        instance.acidity = validated_data.get("acidity", instance.acidity)
        instance.roasting_characteristics = validated_data.get(
            "roasting_characteristics", instance.roasting_characteristics
        )

        password = validated_data.get("password")
        if password:
            instance.set_password(password)
        instance.save()
        return instance


class EmailUniqueCheckSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=ReconiUser.objects.all())],
    )

    class Meta:
        model = ReconiUser
        fields = ["email"]


class NicknameUniqueCheckSerializer(serializers.ModelSerializer):
    nickname = serializers.CharField(
        required=True,
        min_length=1,
        max_length=50,
        validators=[UniqueValidator(queryset=ReconiUser.objects.all())],
    )

    class Meta:
        model = ReconiUser
        fields = ["nickname"]


class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True, write_only=True)
    new_password = serializers.CharField(required=True, write_only=True)

    def validate_new_password(self, value):
        try:
            validate_password(value, self.context["request"].user)
        except ValidationError as e:
            raise serializers.ValidationError(str(e))
        return value

    def validate_old_password(self, value):
        user = self.context["request"].user
        if not user.check_password(value):
            raise serializers.ValidationError("Old password is not correct.")
        return value

    def update(self, instance, validated_data):
        instance.set_password(validated_data["new_password"])
        instance.save()
        return instance
