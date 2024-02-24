from django.urls import path
from . import views


urlpatterns = [
    path('add_user/', views.TelegramUserCreateAPIView.as_view()),
    path('user_lang/<int:user_id>/', views.TelegramUserAPIView.as_view()),
]

