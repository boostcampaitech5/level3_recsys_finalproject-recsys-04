"""
URL configuration for reconi_backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include
from rest_framework import routers
from .views import (
    CoffeeBeanOriginsViewSet,
    CoffeeBeanOriginViewSet,
    CoffeeBeanReviewViewSet,
    CoffeeBeanViewSet,
)

router = routers.DefaultRouter()
router.register(r"coffee-beans", CoffeeBeanViewSet)
router.register(r"bean-origin", CoffeeBeanOriginViewSet)
router.register(r"bean-origins", CoffeeBeanOriginsViewSet)
router.register(r"bean-reviews", CoffeeBeanReviewViewSet)

urlpatterns = [
    # ViewSet 라우터를 추가합니다.
    path("v1/", include(router.urls)),
]
