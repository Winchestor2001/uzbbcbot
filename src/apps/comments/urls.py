from django.urls import path
from . import views


urlpatterns = [
    path('', views.CommentsTemplateView.as_view()),
]

