from rest_framework.serializers import ModelSerializer
from . import models


class TelegramUserSerializer(ModelSerializer):
    class Meta:
        model = models.TgUser
        fields = '__all__'

    def update(self, instance, validated_data):
        print(instance)
        print(validated_data)
        return super().update(instance, validated_data)


class PhoneVerifyCodeSerializer(ModelSerializer):
    class Meta:
        model = models.PhoneVerifyCode
        fields = '__all__'


class RegionsSerializer(ModelSerializer):
    class Meta:
        model = models.Region
        fields = '__all__'

