from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from .serializers import (
    ReconiUserSerializer,
    EmailUniqueCheckSerializer,
    NicknameUniqueCheckSerializer,
)
from django.contrib.auth import get_user_model


ReconiUser = get_user_model()


# 유저 디테일 페이지 데이터 GET, PUT, PATCH
class ReconiUserDetail(generics.RetrieveUpdateAPIView):
    queryset = ReconiUser.objects.all()
    serializer_class = ReconiUserSerializer


class EmailUniqueCheck(generics.CreateAPIView):
    serializer_class = EmailUniqueCheckSerializer

    def post(self, request, format=None):
        serializer = self.get_serializer(
            data=request.data, context={"request": request}
        )

        if serializer.is_valid():
            return Response(
                data={"detail": "You can use this email :)"},
                status=status.HTTP_200_OK,
            )
        else:
            detail = dict()
            detail["detail"] = "This email is alreay Used :("
            return Response(data=detail, status=status.HTTP_400_BAD_REQUEST)


class NickNameUniqueCheck(generics.CreateAPIView):
    serializer_class = NicknameUniqueCheckSerializer

    def post(self, request, format=None):
        serializer = self.get_serializer(
            data=request.data, context={"request": request}
        )

        if serializer.is_valid():
            return Response(
                data={"detail": "You can use this NickName :)"},
                status=status.HTTP_200_OK,
            )
        else:
            detail = dict()
            detail["detail"] = "This NickName is alreay Used :("
            return Response(data=detail, status=status.HTTP_400_BAD_REQUEST)
