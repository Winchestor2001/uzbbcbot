from django.conf import settings
from rest_framework.serializers import ModelSerializer

from core.settings import DOMAIN
from . import models
from .utils import count_ratings


class CitySerializer(ModelSerializer):
    class Meta:
        model = models.City
        fields = ['id', 'uz_name', 'ru_name', 'en_name']


class RegionsSerializer(ModelSerializer):
    class Meta:
        model = models.Region
        fields = '__all__'

    @staticmethod
    def get_cities(obj, lang):
        cities = CitySerializer(instance=models.City.objects.filter(region=obj), many=True)
        return [item[f'{lang}_name'] for item in cities.data]

    def to_representation(self, instance):
        redata = super(RegionsSerializer, self).to_representation(instance)
        lang = self.context.get('lang')
        redata.pop('uz_name')
        redata.pop('ru_name')
        redata.pop('en_name')
        redata['name'] = eval(f'instance.{lang}_name')
        redata['cities'] = self.get_cities(instance, lang)
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
                data['uz_city'] = f"{cities[0].region.uz_name}"
                data['ru_city'] = f"{cities[0].region.ru_name}"
                data['en_city'] = f"{cities[0].region.en_name}"
            else:
                data['uz_city'] = f"{cities[0].uz_name}"
                data['ru_city'] = f"{cities[0].ru_name}"
                data['en_city'] = f"{cities[0].en_name}"
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
    def get_services(obj, lang):
        services = ServiceSerializer(instance=models.Service.objects.filter(category=obj), many=True)
        return [item[f'{lang}_name'] for item in services.data]

    def to_representation(self, instance):
        redata = super(ServiceCategorySerializer, self).to_representation(instance)
        lang = self.context.get('lang')
        redata.pop('uz_name')
        redata.pop('ru_name')
        redata.pop('en_name')
        redata['name'] = eval(f'instance.{lang}_name')
        redata['services'] = self.get_services(instance, lang)
        return redata


class ServiceStuffSerializer(ModelSerializer):
    class Meta:
        model = models.ServiceStuff
        fields = '__all__'

    def to_representation(self, instance):
        data = super(ServiceStuffSerializer, self).to_representation(instance)
        lang = self.context.get('lang')
        data['service'] = eval(f"instance.service.{lang}_name")
        data['city'] = eval(f"instance.city.{lang}_name")
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
        return [item.endswith('name') for item in services.data]

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
        lang = self.context.get('lang')
        data['product'] = eval(f"instance.product.{lang}_name")
        data['city'] = eval(f"instance.city.{lang}_name")
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
        fields = ['uz_video', 'ru_video', 'en_video', 'uz_description', 'ru_description', 'en_description']
    
    def to_representation(self, instance):
        redata = super().to_representation(instance)
        redata['uz_video'] = DOMAIN + instance.video.url
        redata['ru_video'] = DOMAIN + instance.video.url
        redata['en_video'] = DOMAIN + instance.video.url
        return redata
