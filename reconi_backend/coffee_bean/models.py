# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.contrib.auth import get_user_model

ReconiUser = get_user_model()


class CoffeeBeanOrigin(models.Model):
    country = models.CharField(primary_key=True, max_length=30)

    def __str__(self) -> str:
        return str(self.country)

    class Meta:
        managed = False
        db_table = "coffee_bean_origin"


class CoffeeBean(models.Model):
    id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=100, blank=True, null=True)
    aroma = models.FloatField(blank=True, null=True)
    acidity = models.IntegerField(blank=True, null=True)
    sweetness = models.IntegerField(blank=True, null=True)
    body = models.IntegerField(blank=True, null=True)
    balance = models.FloatField(blank=True, null=True)
    roasting_point = models.FloatField(blank=True, null=True)
    roastery = models.CharField(max_length=20, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    coupang_link = models.TextField(blank=True, null=True)

    def __str__(self):
        return str(self.title)

    class Meta:
        managed = False
        db_table = "coffee_bean_bean"


class CoffeeBeanOrigins(models.Model):
    id = models.BigAutoField(primary_key=True)
    bean = models.ForeignKey(CoffeeBean, models.DO_NOTHING)
    origin = models.ForeignKey("CoffeeBeanOrigin", models.DO_NOTHING)

    def __str__(self):
        return str(self.origin.country)

    class Meta:
        managed = False
        db_table = "coffee_bean_bean_origins"
        unique_together = (("bean", "origin"),)


class CoffeeBeanReview(models.Model):
    title = models.CharField(max_length=100, blank=True, null=True)
    user_nickname = models.CharField(max_length=20, blank=True, null=True)
    rating = models.IntegerField(blank=True, null=True)
    content = models.TextField(blank=True, null=True)
    taste_satisfaction = models.CharField(max_length=20, blank=True, null=True)
    bean_id = models.ForeignKey(CoffeeBean, models.DO_NOTHING)

    def __str__(self):
        return str(self.user_nickname + "-" + self.bean_id.title)

    class Meta:
        managed = False
        db_table = "coffee_bean_beanreview"


class CoffeeInCart(models.Model):
    user = models.OneToOneField(
        ReconiUser, primary_key=True, on_delete=models.CASCADE
    )
    coffee_beans = models.ManyToManyField(CoffeeBean)

    class Meta:
        managed = False
        db_table = "coffee_in_cart"

    def __str__(self):
        return str(self.user.nickname + " - Cart")


class UserImplicit(models.Model):
    """
    User Implicit FeedBack
    - 회원이 구매 페이지까지 연결된 커피 아이템
    """

    user = models.OneToOneField(
        ReconiUser, primary_key=True, on_delete=models.CASCADE
    )
    coffee_beans = models.ManyToManyField(CoffeeBean)

    class Meta:
        managed = True
        db_table = "user_implicit"

    def __str__(self):
        return str(self.user.nickname + " - Implicit")


class RecommendedCoffeeColdStart(models.Model):
    """
    Cold Start User Recommendated Coffee Item
    - Cold Start 유저에게 추천된 커피 원두 아이템 리스트
    """

    user = models.OneToOneField(
        ReconiUser, primary_key=True, on_delete=models.CASCADE
    )
    coffee_beans = models.ManyToManyField(CoffeeBean)

    class Meta:
        managed = True
        db_table = "rec_coffee_cold_start"

    def __str__(self):
        return str(self.user.nickname + " - Recommended Coffees")


class RecommendedCoffeeUserItem(models.Model):
    """
    User-Item Interaction Recommendated Coffee Item
    -  유저-아이템 Interaction 기반 추천된 커피 원두 아이템 리스트
    """

    user = models.OneToOneField(
        ReconiUser, primary_key=True, on_delete=models.CASCADE
    )
    coffee_beans = models.ManyToManyField(CoffeeBean)

    class Meta:
        managed = True
        db_table = "rec_coffee_user_item"

    def __str__(self):
        return str(self.user.nickname + " - Recommended Coffees")
