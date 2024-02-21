from django.contrib import admin
from . import models


@admin.register(models.TgUser)
class TgUserAdmin(admin.ModelAdmin):
    list_display = ['user_id', 'username', 'is_active', 'language']
    list_display_links = ['user_id', 'username']


@admin.register(models.Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    list_display_links = ['name']


@admin.register(models.Professional)
class ProfessionalAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    list_display_links = ['name']


@admin.register(models.Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['id', 'fullname', 'region', 'professional', 'price']
    list_display_links = ['fullname', 'region']


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'price']
    list_display_links = ['name']


@admin.register(models.Market)
class MarketAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'product']
    list_display_links = ['name', 'product']


@admin.register(models.Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ['id', 'tg_user', 'rating', 'comment']
    list_display_links = ['tg_user']

