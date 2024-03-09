from django.urls import path
from . import views


urlpatterns = [
    path('add_user/', views.TelegramUserCreateAPIView.as_view()),
    path('user_info/<int:user_id>/', views.TelegramUserCreateAPIView.as_view()),
    path('user_lang/<int:user_id>/', views.TelegramUserAPIView.as_view()),
    path('regions/', views.RegionsAPIView.as_view()),
    path('verify_user/', views.UpdateUserInfoAPIView.as_view()),
    path('search_service/', views.SearchServiceAPIView.as_view()),
    path('get_services/', views.GetAllServiceAPIView.as_view()),

    path('call/', views.CallAPIView.as_view()),
]

