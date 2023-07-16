from django.contrib import admin
from .models import (
    CoffeeBean,
    CoffeeBeanOrigins,
    CoffeeBeanReview,
    CoffeeBeanOrigin,
)

# Register your models here.
admin.site.register(CoffeeBean)
admin.site.register(CoffeeBeanOrigins)
admin.site.register(CoffeeBeanReview)
admin.site.register(CoffeeBeanOrigin)
