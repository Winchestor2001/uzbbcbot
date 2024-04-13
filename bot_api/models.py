from django.db import models

from core.settings import DB_LANGUAGES


class CustomBaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True


class Region(CustomBaseModel):
    uz_name = models.CharField(max_length=100)
    ru_name = models.CharField(max_length=100, blank=True, null=True)
    en_name = models.CharField(max_length=100, blank=True, null=True)
    is_visible = models.BooleanField(default=True)

    def __str__(self):
        return self.uz_name


class City(CustomBaseModel):
    uz_name = models.CharField(max_length=100)
    ru_name = models.CharField(max_length=100, blank=True, null=True)
    en_name = models.CharField(max_length=100, blank=True, null=True)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)

    def __str__(self):
        return self.uz_name


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
    uz_name = models.CharField(max_length=200)
    ru_name = models.CharField(max_length=200, blank=True, null=True)
    en_name = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.uz_name


class Product(CustomBaseModel):
    uz_name = models.CharField(max_length=200)
    ru_name = models.CharField(max_length=200, blank=True, null=True)
    en_name = models.CharField(max_length=200, blank=True, null=True)
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)

    def __str__(self):
        return self.uz_name


class ServiceCategory(CustomBaseModel):
    uz_name = models.CharField(max_length=200)
    ru_name = models.CharField(max_length=200, blank=True, null=True)
    en_name = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.uz_name


class Service(CustomBaseModel):
    uz_name = models.CharField(max_length=200)
    ru_name = models.CharField(max_length=200, blank=True, null=True)
    en_name = models.CharField(max_length=200, blank=True, null=True)
    category = models.ForeignKey(ServiceCategory, on_delete=models.CASCADE)

    def __str__(self):
        return self.uz_name


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
    lang = models.CharField(choices=DB_LANGUAGES, max_length=50)

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
    lang = models.CharField(choices=DB_LANGUAGES, max_length=50)

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
    uz_video = models.FileField(upload_to='uz_video/', blank=True, null=True)
    ru_video = models.FileField(upload_to='ru_video/', blank=True, null=True)
    en_video = models.FileField(upload_to='en_video/', blank=True, null=True)
    uz_description = models.TextField(blank=True, null=True)
    ru_description = models.TextField(blank=True, null=True)
    en_description = models.TextField(blank=True, null=True)
    comment_request_time = models.PositiveIntegerField(default=1)

    def __str__(self):
        return "About Bot"

    