from rest_framework.serializers import ModelSerializer
from . import models


class TelegramUserSerializer(ModelSerializer):
    class Meta:
        model = models.TgUser
        fields = '__all__'

