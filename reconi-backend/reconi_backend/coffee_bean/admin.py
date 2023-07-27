from django.contrib import admin
from .models import (
    CoffeeBean,
    CoffeeBeanOrigins,
    CoffeeBeanReview,
    CoffeeBeanOrigin,
    CoffeeInCart,
    RecommendedCoffeeColdStart,
    RecommendedCoffeeNotColdStart,
    UserImplicit,
)

# Register your models here.
admin.site.register(CoffeeBean)
admin.site.register(CoffeeBeanOrigins)
admin.site.register(CoffeeBeanReview)
admin.site.register(CoffeeBeanOrigin)
admin.site.register(CoffeeInCart)
admin.site.register(RecommendedCoffeeColdStart)
admin.site.register(RecommendedCoffeeNotColdStart)
admin.site.register(UserImplicit)
