from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models


class Region(models.Model):
    name = models.CharField(max_length=100)
    is_visible = models.BooleanField(default=True)

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
    region = models.ForeignKey(Region, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.user_id} - {self.username}"


class Professional(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Service(models.Model):
    fullname = models.CharField(max_length=100)
    region = models.ForeignKey(Region, on_delete=models.SET_NULL, blank=True, null=True)
    professional = models.ForeignKey(Professional, on_delete=models.SET_NULL, blank=True, null=True)
    price = models.FloatField()
    latitude = models.CharField(max_length=200, null=True, blank=True)
    longitude = models.CharField(max_length=200, null=True, blank=True)
    phone_number = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.fullname


class Product(models.Model):
    name = models.CharField(max_length=200)
    price = models.FloatField()

    def __str__(self):
        return self.name


class ServiceWorkTime(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    from_date = models.TimeField()
    to_date = models.TimeField()

    def __str__(self):
        return self.service


class Market(models.Model):
    name = models.CharField(max_length=200)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True, null=True)
    latitude = models.CharField(max_length=200, null=True, blank=True)
    longitude = models.CharField(max_length=200, null=True, blank=True)
    phone_number = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.name


class MarketWorkTime(models.Model):
    service = models.ForeignKey(Market, on_delete=models.CASCADE)
    from_date = models.TimeField()
    to_date = models.TimeField()

    def __str__(self):
        return self.service


class Rating(models.Model):
    tg_user = models.ForeignKey(TgUser, on_delete=models.CASCADE)
    rating = models.FloatField()
    comment = models.CharField(max_length=250)

    def __str__(self):
        return f"{self.tg_user} - {self.rating}"


class PhoneVerifyCode(models.Model):
    tg_user = models.ForeignKey(TgUser, on_delete=models.CASCADE)
    code = models.IntegerField()

    def __str__(self):
        return f"{self.tg_user} - {self.code}"

