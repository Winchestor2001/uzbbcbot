from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models


class CustomBaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True


class Region(CustomBaseModel):
    name = models.CharField(max_length=100)
    is_visible = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class City(CustomBaseModel):
    name = models.CharField(max_length=100)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class TgUser(CustomBaseModel):
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
    city = models.ManyToManyField(City, null=True, blank=True)
    all_regions = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user_id} - {self.username}"


class ProductCategory(CustomBaseModel):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Product(CustomBaseModel):
    name = models.CharField(max_length=200)
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class ServiceCategory(CustomBaseModel):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Service(CustomBaseModel):
    name = models.CharField(max_length=200)
    category = models.ForeignKey(ServiceCategory, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class ServiceStuff(CustomBaseModel):
    fullname = models.CharField(max_length=100)
    service = models.ForeignKey(Service, on_delete=models.SET_NULL, blank=True, null=True)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, blank=True, null=True)
    experience = models.PositiveIntegerField(blank=True, null=True)
    price = models.FloatField(default=0)
    phone_number = models.CharField(max_length=50, null=True, blank=True)
    rating = models.FloatField(default=0.0)
    description = models.TextField(blank=True, null=True)
    location_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.fullname


class ProductDetail(CustomBaseModel):
    fullname = models.CharField(max_length=200)
    from_price = models.FloatField()
    to_price = models.FloatField()
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True, null=True)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, blank=True, null=True)
    phone_number = models.CharField(max_length=50, null=True, blank=True)
    rating = models.FloatField(default=0.0)
    description = models.TextField(blank=True, null=True)
    location_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.fullname


class ServiceRating(CustomBaseModel):
    tg_user = models.ForeignKey(TgUser, on_delete=models.CASCADE)
    stuff = models.ForeignKey(ServiceStuff, on_delete=models.CASCADE)
    rating = models.IntegerField()
    comment = models.CharField(max_length=250)

    def __str__(self):
        return f"{self.tg_user} - {self.rating}"


class ProductRating(CustomBaseModel):
    tg_user = models.ForeignKey(TgUser, on_delete=models.CASCADE)
    product_detail = models.ForeignKey(ProductDetail, on_delete=models.CASCADE)
    rating = models.IntegerField()
    comment = models.CharField(max_length=250)

    def __str__(self):
        return f"{self.tg_user} - {self.rating}"


class AboutBot(CustomBaseModel):
    video = models.FileField(upload_to='video/')
    description = models.TextField()
    comment_request_time = models.PositiveIntegerField(default=1)

    def __str__(self):
        return "About Bot"

    