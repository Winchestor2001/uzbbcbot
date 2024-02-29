import random

from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from bot_api.serializers import TelegramUserSerializer, PhoneVerifyCodeSerializer, RegionsSerializer
from . import models


class TelegramUserCreateAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        user_id = request.GET.get('user_id')
        tg_user = models.TgUser.objects.filter(user_id=user_id)
        serializer = TelegramUserSerializer(instance=tg_user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        user_id = request.data.get('user_id')
        tg_user = models.TgUser.objects.filter(user_id=user_id)
        if tg_user.exists():
            serializer = TelegramUserSerializer(instance=tg_user.first())
            stat = status.HTTP_200_OK
        else:
            serializer = TelegramUserSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            stat = status.HTTP_201_CREATED
        return Response(serializer.data, status=stat)


class TelegramUserAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = TelegramUserSerializer
    permission_classes = [permissions.AllowAny]
    queryset = models.TgUser
    lookup_field = 'user_id'


class PhoneVerifyCodeAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        user_phone_number = request.data['phone_number']
        data = {
            "tg_user": request.data['user_id'],
            "code": random.randint(1000, 99999)
        }
        print(data)
        serializer = PhoneVerifyCodeSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class RegionsAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        regions = models.Region.objects.filter(is_visible=True)
        serializer = RegionsSerializer(instance=regions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UpdateUserInfoAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def patch(self, request):
        user_id = request.data['user_id']
        phone_number = request.data['phone_number']
        region = request.data['region']
        user = models.TgUser.objects.get(user_id=int(user_id))
        user.phone_number = phone_number
        user.region = models.Region.objects.get(name=region)
        user.is_active = True
        user.save()
        serializer = TelegramUserSerializer(instance=user)
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)


