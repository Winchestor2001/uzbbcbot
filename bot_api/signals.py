from django.db.models.signals import pre_save, pre_delete, post_delete
from django.dispatch import receiver
from . import models
from .utils import count_ratings


@receiver(pre_save, sender=models.ServiceRating)
def pre_save_handler(sender, instance, **kwargs):
    stuff = models.ServiceStuff.objects.get(id=instance.stuff.id)
    ratings = models.ServiceRating.objects.filter(stuff=stuff)
    result = count_ratings(ratings)
    stuff.rating = result
    stuff.save()


@receiver(post_delete, sender=models.ServiceRating)
def pre_delete_handler(sender, instance, **kwargs):
    stuff = models.ServiceStuff.objects.get(id=instance.stuff.id)
    ratings = models.ServiceRating.objects.filter(stuff=stuff)
    result = count_ratings(ratings)
    stuff.rating = result
    stuff.save()
