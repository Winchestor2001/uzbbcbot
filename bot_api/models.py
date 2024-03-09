from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models


class Region(models.Model):
    name = models.CharField(max_length=100)
    is_visible = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class City(models.Model):
    name = models.CharField(max_length=100)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class TgUser(models.Model):
    LANGUAGES = (
        ('uz', 'uz'),
        ('ru', 'ru'),
        ('en', 'en'),
        ('null', 'null'),
    )
    user_id = models.BigIntegerField(primary_key=True)
    username = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=50, blank=True, null=True)
    is_active = models.BooleanField(default=False)
    language = models.CharField(max_length=10, choices=LANGUAGES, default='uz')
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, blank=True)
    all_regions = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user_id} - {self.username}"


class ProductCategory(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=200)
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class ServiceCategory(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Service(models.Model):
    name = models.CharField(max_length=200)
    category = models.ForeignKey(ServiceCategory, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class ServiceStuff(models.Model):
    fullname = models.CharField(max_length=100)
    service = models.ForeignKey(Service, on_delete=models.SET_NULL, blank=True, null=True)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, blank=True, null=True)
    experience = models.DateField(blank=True, null=True)
    price = models.FloatField()
    phone_number = models.CharField(max_length=50, null=True, blank=True)
    from_date = models.TimeField()
    to_date = models.TimeField()
    rating = models.FloatField(default=0.0)

    def __str__(self):
        return self.fullname


class ProductDetail(models.Model):
    name = models.CharField(max_length=200)
    from_price = models.FloatField()
    to_price = models.FloatField()
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True, null=True)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, blank=True, null=True)
    phone_number = models.CharField(max_length=50, null=True, blank=True)
    rating = models.FloatField(default=0.0)

    def __str__(self):
        return self.name


class ServiceRating(models.Model):
    tg_user = models.ForeignKey(TgUser, on_delete=models.CASCADE)
    stuff = models.ForeignKey(ServiceStuff, on_delete=models.CASCADE)
    rating = models.FloatField()
    comment = models.CharField(max_length=250)

    def __str__(self):
        return f"{self.tg_user} - {self.rating}"


class ProductRating(models.Model):
    tg_user = models.ForeignKey(TgUser, on_delete=models.CASCADE)
    product_detail = models.ForeignKey(ProductDetail, on_delete=models.CASCADE)
    rating = models.FloatField()
    comment = models.CharField(max_length=250)

