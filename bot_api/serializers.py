from rest_framework.serializers import ModelSerializer
from . import models


class CitySerializer(ModelSerializer):
    class Meta:
        model = models.City
        fields = ['name']


class RegionsSerializer(ModelSerializer):
    class Meta:
        model = models.Region
        fields = '__all__'

    @staticmethod
    def get_cities(obj):
        cities = CitySerializer(instance=models.City.objects.filter(region=obj), many=True)
        return [item['name'] for item in cities.data]

    def to_representation(self, instance):
        redata = super(RegionsSerializer, self).to_representation(instance)
        redata['cities'] = self.get_cities(instance)
        return redata


class TelegramUserSerializer(ModelSerializer):
    class Meta:
        model = models.TgUser
        fields = '__all__'

    def to_representation(self, instance):
        data = super(TelegramUserSerializer, self).to_representation(instance)
        if instance.city:
            data['city'] = f"{instance.city.region.name} - {instance.city.name}"
        return data


class ServiceSerializer(ModelSerializer):
    class Meta:
        model = models.Service
        fields = '__all__'

    def to_representation(self, instance):
        data = super(ServiceSerializer, self).to_representation(instance)
        data['professional'] = instance.professional.name
        data['region'] = instance.region.name
        return data

