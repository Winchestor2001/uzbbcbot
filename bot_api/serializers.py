from rest_framework.serializers import ModelSerializer
from . import models


class TelegramUserSerializer(ModelSerializer):
    class Meta:
        model = models.TgUser
        fields = '__all__'


class PhoneVerifyCodeSerializer(ModelSerializer):
    class Meta:
        model = models.PhoneVerifyCode
        fields = '__all__'

    def create(self, validated_data):
        print(validated_data)
        return models.PhoneVerifyCode.objects.create(**validated_data)