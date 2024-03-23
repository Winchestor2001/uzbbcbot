from django.contrib import admin
from . import models
from django.db.models import QuerySet


admin.site.site_header = "Bot Admin Panel"
admin.site.site_title = "Bot Admin Panel"


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
    ordering = ['-created_at']
    search_fields = ['user_id', 'username']


@admin.register(models.Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'is_visible']
    list_display_links = ['name']
    inlines = [CityInline]
    ordering = ['-created_at']
    actions = ['set_visible', 'set_unvisible']

    @admin.action(description="Set True")
    def set_visible(self, request, qs: QuerySet):
        qs.update(is_visible=True)
    

    @admin.action(description="Set False")
    def set_unvisible(self, request, qs: QuerySet):
        qs.update(is_visible=False)


@admin.register(models.ServiceCategory)
class ServiceCategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    list_display_links = ['name']
    inlines = [ServiceInline]
    ordering = ['-created_at']


@admin.register(models.ServiceStuff)
class ServiceStuffAdmin(admin.ModelAdmin):
    list_display = ['id', 'fullname', 'city', 'service', 'price', 'rating']
    list_display_links = ['fullname', 'city']
    readonly_fields = ['rating']
    ordering = ['-created_at']
    search_fields = ['fullname']

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['experience'].widget.attrs['placeholder'] = 'YYYY (2024)'
        return form


@admin.register(models.ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    list_display_links = ['name']
    inlines = [ProductInline]
    ordering = ['-created_at']


@admin.register(models.ProductDetail)
class ProductDetailAdmin(admin.ModelAdmin):
    list_display = ['id', 'fullname', 'product']
    list_display_links = ['fullname', 'product']
    readonly_fields = ['rating']
    ordering = ['-created_at']
    search_fields = ['fullname']


@admin.register(models.ServiceRating)
class ServiceRatingAdmin(admin.ModelAdmin):
    list_display = ['id', 'tg_user', 'stuff', 'rating', 'comment']
    list_display_links = ['tg_user']
    ordering = ['-created_at']


@admin.register(models.ProductRating)
class ProductRatingAdmin(admin.ModelAdmin):
    list_display = ['id', 'tg_user', 'product_detail', 'rating', 'comment']
    list_display_links = ['tg_user']
    ordering = ['-created_at']


@admin.register(models.AboutBot)
class AboutBotAdmin(admin.ModelAdmin):
    list_display = ['id']

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['comment_request_time'].widget.attrs['placeholder'] = 'Only in minute'
        return form
