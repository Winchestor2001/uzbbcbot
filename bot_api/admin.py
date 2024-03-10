from django.contrib import admin
from . import models


class CityInline(admin.TabularInline):
    model = models.City
    extra = 1


class ServiceInline(admin.TabularInline):
    model = models.Service
    extra = 1


class ProductInline(admin.TabularInline):
    model = models.Product
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


@admin.register(models.ServiceCategory)
class ServiceCategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    list_display_links = ['name']
    inlines = [ServiceInline]


@admin.register(models.ServiceStuff)
class ServiceStuffAdmin(admin.ModelAdmin):
    list_display = ['id', 'fullname', 'city', 'service', 'price', 'rating']
    list_display_links = ['fullname', 'city']
    readonly_fields = ['rating']


@admin.register(models.ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    list_display_links = ['name']
    inlines = [ProductInline]


@admin.register(models.ProductDetail)
class ProductDetailAdmin(admin.ModelAdmin):
    list_display = ['id', 'fullname', 'product']
    list_display_links = ['fullname', 'product']
    readonly_fields = ['rating']


@admin.register(models.ServiceRating)
class ServiceRatingAdmin(admin.ModelAdmin):
    list_display = ['id', 'tg_user', 'stuff', 'rating', 'comment']
    list_display_links = ['tg_user']


@admin.register(models.ProductRating)
class ProductRatingAdmin(admin.ModelAdmin):
    list_display = ['id', 'tg_user', 'product_detail', 'rating', 'comment']
    list_display_links = ['tg_user']


