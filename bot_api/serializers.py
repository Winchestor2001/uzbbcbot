from rest_framework.serializers import ModelSerializer
from . import models
from .utils import count_ratings


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


class ServiceCategorySerializer(ModelSerializer):
    class Meta:
        model = models.ServiceCategory
        fields = '__all__'

    @staticmethod
    def get_services(obj):
        services = ServiceSerializer(instance=models.Service.objects.filter(category=obj), many=True)
        return [item['name'] for item in services.data]

    def to_representation(self, instance):
        redata = super(ServiceCategorySerializer, self).to_representation(instance)
        redata['services'] = self.get_services(instance)
        return redata


class ServiceStuffSerializer(ModelSerializer):
    class Meta:
        model = models.ServiceStuff
        fields = '__all__'

    @staticmethod
    def get_rating(obj):
        ratings = models.ServiceRating.objects.filter(stuff=obj)
        result = count_ratings(ratings)
        return result

    def to_representation(self, instance):
        data = super(ServiceStuffSerializer, self).to_representation(instance)
        data['service'] = instance.service.name
        data['city'] = instance.city.name
        # data['rating'] = self.get_rating(instance)
        return data

