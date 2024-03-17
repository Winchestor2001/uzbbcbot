from django.db import models
from bot_api.models import TgUser, ServiceStuff, ProductDetail


class NotifyTasks(models.Model):
    TYPE = (
        ('service', 'service'),
        ('product', 'product'),
    )
    user = models.ForeignKey(TgUser, on_delete=models.CASCADE)
    receiver = models.IntegerField()
    type = models.CharField(max_length=50, choices=TYPE)
    created_at = models.TimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user}"
