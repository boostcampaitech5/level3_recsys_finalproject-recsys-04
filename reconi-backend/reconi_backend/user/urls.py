from django.urls import path, include
from .views import EmailUniqueCheck, NickNameUniqueCheck, ReconiUserDetail

urlpatterns = [
    path("", include("dj_rest_auth.urls")),
    path("registration/", include("dj_rest_auth.registration.urls")),
    path("user_detail/<str:pk>/", ReconiUserDetail.as_view()),
    path("registration/email-check/", EmailUniqueCheck.as_view()),
    path("registration/nickname-check/", NickNameUniqueCheck.as_view()),
]
