from django.urls import path
from . import views


urlpatterns = [
    path('add_user/', views.TelegramUserCreateAPIView.as_view()),
    path('user_info/<int:user_id>/', views.TelegramUserCreateAPIView.as_view()),
    path('user_lang/<int:user_id>/', views.TelegramUserAPIView.as_view()),
    path('regions/', views.RegionsAPIView.as_view()),
    path('verify_user/', views.UpdateUserInfoAPIView.as_view()),
    path('search_services/', views.SearchServiceAPIView.as_view()),
    path('get_services/', views.GetAllServiceAPIView.as_view()),
    path('stuff_service/', views.StuffServiceAPIView.as_view()),
    path('stuff_comments/', views.StuffCommentsAPIView.as_view()),
    path('get_products/', views.GetAllProductAPIView.as_view()),
    path('search_products/', views.SearchProductAPIView.as_view()),
    path('product_info/', views.ProductInfoAPIView.as_view()),
    path('product_comments/', views.ProductCommentsAPIView.as_view()),
    path('search/', views.SearchAPIView.as_view()),
    path('about_bot/', views.AboutBotAPIView.as_view()),
    path('get_cities/', views.GetCities.as_view(), name="cities-api"),

    path('call/', views.CallAPIView.as_view()),
    
    path('get_service_excel/', views.get_service_excel, name="get_service_excel"),
    path('get_product_excel/', views.get_product_excel, name="get_product_excel"),
]

