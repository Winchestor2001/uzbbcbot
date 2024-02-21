from django.db import models


class Region(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class TgUser(models.Model):
    user_id = models.BigIntegerField(primary_key=True)
    username = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=50)
    is_active = models.BooleanField(default=False)
    language = models.CharField(max_length=10)

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

    def __str__(self):
        return self.fullname


class Product(models.Model):
    name = models.CharField(max_length=200)
    price = models.FloatField()

    def __str__(self):
        return self.name


class Market(models.Model):
    name = models.CharField(max_length=200)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.name


class Rating(models.Model):
    tg_user = models.ForeignKey(TgUser, on_delete=models.CASCADE)
    rating = models.FloatField()
    comment = models.CharField(max_length=250)

    def __str__(self):
        return f"{self.tg_user} - {self.rating}"

