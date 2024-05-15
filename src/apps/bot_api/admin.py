from django.contrib import admin
from django.contrib.auth.models import User, Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from unfold.admin import ModelAdmin
from unfold.forms import AdminPasswordChangeForm, UserChangeForm, UserCreationForm
from unfold.admin import ModelAdmin, TabularInline
from django.http import HttpRequest
from . import models
from django.db.models import QuerySet


admin.site.site_header = "Bot Admin Panel"
admin.site.site_title = "Bot Admin Panel"



class CityInline(TabularInline):
    model = models.City
    extra = 1


class ServiceInline(TabularInline):
    model = models.Service
    extra = 1


class ProductInline(TabularInline):
    model = models.Product
    extra = 1


@admin.register(models.TgUser)
class TgUserAdmin(ModelAdmin):
    list_display = ['user_id', 'username', 'is_active', 'language']
    list_display_links = ['user_id', 'username']
    ordering = ['-created_at']
    search_fields = ['user_id', 'username']


@admin.register(models.Region)
class RegionAdmin(ModelAdmin):
    list_display = ['id', 'uz_name', 'is_visible']
    list_display_links = ['uz_name']
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
class ServiceCategoryAdmin(ModelAdmin):
    list_display = ['id', 'uz_name']
    list_display_links = ['uz_name']
    inlines = [ServiceInline]
    ordering = ['-created_at']


@admin.register(models.ServiceStuff)
class ServiceStuffAdmin(ModelAdmin):
    list_display = ['id', 'fullname', 'city', 'service', 'price', 'rating', "lang"]
    list_display_links = ['fullname', 'city']
    readonly_fields = ['rating']
    ordering = ['-created_at']
    search_fields = ['fullname']
    list_filter = ["city", "service", "lang"]

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['experience'].widget.attrs['placeholder'] = 'YYYY (2024)'
        return form


@admin.register(models.ProductCategory)
class ProductCategoryAdmin(ModelAdmin):
    list_display = ['id', 'uz_name']
    list_display_links = ['uz_name']
    inlines = [ProductInline]
    ordering = ['-created_at']


@admin.register(models.ProductDetail)
class ProductDetailAdmin(ModelAdmin):
    list_display = ['id', 'fullname', 'product', "lang"]
    list_display_links = ['fullname', 'product']
    readonly_fields = ['rating']
    ordering = ['-created_at']
    search_fields = ['fullname']
    list_filter = ["city", "product", "lang"]


@admin.register(models.ServiceRating)
class ServiceRatingAdmin(ModelAdmin):
    list_display = ['id', 'tg_user', 'stuff', 'rating', 'comment']
    list_display_links = ['tg_user']
    ordering = ['-created_at']


@admin.register(models.ProductRating)
class ProductRatingAdmin(ModelAdmin):
    list_display = ['id', 'tg_user', 'product_detail', 'rating', 'comment']
    list_display_links = ['tg_user']
    ordering = ['-created_at']


@admin.register(models.AboutBot)
class AboutBotAdmin(ModelAdmin):
    
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['comment_request_time'].widget.attrs['placeholder'] = 'Only in minute'
        return form

    def has_add_permission(self, request: HttpRequest) -> bool:
        count_obj = models.AboutBot.objects.count()
        return count_obj == 0
    

admin.site.unregister(User)
admin.site.unregister(Group)
admin.site.register(Group, ModelAdmin)


@admin.register(User)
class UserAdmin(BaseUserAdmin, ModelAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    change_password_form = AdminPasswordChangeForm