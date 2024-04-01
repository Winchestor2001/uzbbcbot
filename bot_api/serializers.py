from django.conf import settings
from rest_framework.serializers import ModelSerializer

from core.settings import DOMAIN
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
        if instance.city.all():
            cities = instance.city.all()
            if cities.count() > 1:
                data['city'] = f"{cities[0].region.name}"
            else:
                data['city'] = f"{cities[0].name}"
        return data


class ServiceSerializer(ModelSerializer):
    class Meta:
        model = models.Service
        fields = '__all__'


class ProductSerializer(ModelSerializer):
    class Meta:
        model = models.Product
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

    def to_representation(self, instance):
        data = super(ServiceStuffSerializer, self).to_representation(instance)
        data['service'] = instance.service.name
        data['city'] = instance.city.name
        return data


class StuffCommentsSerializer(ModelSerializer):
    class Meta:
        model = models.ServiceRating
        fields = ['tg_user', 'comment', 'rating']

    def to_representation(self, instance):
        data = super(StuffCommentsSerializer, self).to_representation(instance)
        data['tg_user'] = "**" + instance.tg_user.username[2:]
        return data


class ProductCategorySerializer(ModelSerializer):
    class Meta:
        model = models.ServiceCategory
        fields = '__all__'

    @staticmethod
    def get_products(obj):
        services = ProductSerializer(instance=models.Product.objects.filter(category=obj), many=True)
        return [item['name'] for item in services.data]

    def to_representation(self, instance):
        redata = super(ProductCategorySerializer, self).to_representation(instance)
        redata['products'] = self.get_products(instance)
        return redata


class ProductDetailSerializer(ModelSerializer):
    class Meta:
        model = models.ProductDetail
        fields = '__all__'

    def to_representation(self, instance):
        data = super(ProductDetailSerializer, self).to_representation(instance)
        data['product'] = instance.product.name
        data['city'] = instance.city.name
        return data


class ProductCommentsSerializer(ModelSerializer):
    class Meta:
        model = models.ProductRating
        fields = ['tg_user', 'comment']

    def to_representation(self, instance):
        data = super(ProductCommentsSerializer, self).to_representation(instance)
        data['tg_user'] = "**" + instance.tg_user.username[2:]
        return data


class AboutBotSerializer(ModelSerializer):
    class Meta:
        model = models.AboutBot
        fields = ['video', 'description']
    
    def to_representation(self, instance):
        redata = super().to_representation(instance)
        redata['video'] = DOMAIN + instance.video.url
        return redata
