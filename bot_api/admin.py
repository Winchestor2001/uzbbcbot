from django.contrib import admin
from . import models


class ServiceWorkTimeInline(admin.TabularInline):
    model = models.ServiceWorkTime
    extra = 1


class MarketWorkTimeInline(admin.TabularInline):
    model = models.MarketWorkTime
    extra = 1


class CityInline(admin.TabularInline):
    model = models.City
    extra = 1


@admin.register(models.TgUser)
class TgUserAdmin(admin.ModelAdmin):
    list_display = ['user_id', 'username', 'is_active', 'language']
    list_display_links = ['user_id', 'username']


@admin.register(models.Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    list_display_links = ['name']
    inlines = [CityInline]


@admin.register(models.Professional)
class ProfessionalAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    list_display_links = ['name']


@admin.register(models.Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['id', 'fullname', 'region', 'professional', 'price']
    list_display_links = ['fullname', 'region']
    inlines = [ServiceWorkTimeInline]


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'price']
    list_display_links = ['name']


@admin.register(models.Market)
class MarketAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'product']
    list_display_links = ['name', 'product']
    inlines = [MarketWorkTimeInline]


@admin.register(models.ServiceRating)
class ServiceRatingAdmin(admin.ModelAdmin):
    list_display = ['id', 'tg_user', 'service', 'rating', 'comment']
    list_display_links = ['tg_user']


@admin.register(models.MarketRating)
class MarketRatingAdmin(admin.ModelAdmin):
    list_display = ['id', 'tg_user', 'market', 'rating', 'comment']
    list_display_links = ['tg_user']


