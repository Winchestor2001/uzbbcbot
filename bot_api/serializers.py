from rest_framework.serializers import ModelSerializer
from . import models


class RegionsSerializer(ModelSerializer):
    class Meta:
        model = models.Region
        fields = '__all__'


class TelegramUserSerializer(ModelSerializer):
    region = RegionsSerializer()

    class Meta:
        model = models.TgUser
        fields = '__all__'


class PhoneVerifyCodeSerializer(ModelSerializer):
    class Meta:
        model = models.PhoneVerifyCode
        fields = '__all__'


class ServiceSerializer(ModelSerializer):
    class Meta:
        model = models.Service
        fields = '__all__'

    def to_representation(self, instance):
        data = super(ServiceSerializer, self).to_representation(instance)
        data['professional'] = instance.professional.name
        return data

