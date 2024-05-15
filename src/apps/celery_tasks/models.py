from django.db import models
from bot_api.models import TgUser, ServiceStuff, ProductDetail, CustomBaseModel


class NotifyTasks(CustomBaseModel):
    TYPE = (
        ('service', 'service'),
        ('product', 'product'),
    )
    user = models.ForeignKey(TgUser, on_delete=models.CASCADE)
    receiver = models.IntegerField()
    type = models.CharField(max_length=50, choices=TYPE)

    def __str__(self):
        return f"{self.user}"
