from rest_framework import viewsets

# Import Models
from .models import (
    CoffeeBeanOrigin,
    CoffeeBean,
    CoffeeBeanOrigins,
    CoffeeBeanReview,
)

# Import Serializers
from .serializers import (
    CoffeeBeanSerializer,
    CoffeeBeanOriginSerializer,
    CoffeeBeanOriginsSerializer,
    CoffeeBeanReviewSerializer,
)


# Create your views here.
class CoffeeBeanOriginViewSet(viewsets.ModelViewSet):
    queryset = CoffeeBeanOrigin.objects.all()
    serializer_class = CoffeeBeanOriginSerializer


class CoffeeBeanViewSet(viewsets.ModelViewSet):
    queryset = CoffeeBean.objects.all()
    serializer_class = CoffeeBeanSerializer


class CoffeeBeanOriginsViewSet(viewsets.ModelViewSet):
    queryset = CoffeeBeanOrigins.objects.all()
    serializer_class = CoffeeBeanOriginsSerializer


class CoffeeBeanReviewViewSet(viewsets.ModelViewSet):
    queryset = CoffeeBeanReview.objects.all()
    serializer_class = CoffeeBeanReviewSerializer
