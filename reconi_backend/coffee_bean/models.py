# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class CoffeeBeanBean(models.Model):
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

    class Meta:
        managed = False
        db_table = "coffee_bean_bean"


class CoffeeBeanBeanOrigins(models.Model):
    id = models.BigAutoField(primary_key=True)
    bean = models.ForeignKey(CoffeeBeanBean, models.DO_NOTHING)
    origin = models.ForeignKey("CoffeeBeanOrigin", models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "coffee_bean_bean_origins"
        unique_together = (("bean", "origin"),)


class CoffeeBeanBeanreview(models.Model):
    title = models.CharField(max_length=100, blank=True, null=True)
    user_nickname = models.CharField(max_length=20, blank=True, null=True)
    rating = models.IntegerField(blank=True, null=True)
    content = models.TextField(blank=True, null=True)
    taste_satisfication = models.CharField(max_length=20, blank=True, null=True)
    bean_id = models.ForeignKey(CoffeeBeanBean, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "coffee_bean_beanreview"


class CoffeeBeanOrigin(models.Model):
    country = models.CharField(primary_key=True, max_length=30)

    class Meta:
        managed = False
        db_table = "coffee_bean_origin"
