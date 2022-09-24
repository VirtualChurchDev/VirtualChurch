from django.urls import path
from . import views

app_name = "church"

urlpatterns = [
    path('', views.home, name='home'),
    path('pricing/', views.pricing, name='pricing'),
    path('newsall/', views.newsall, name='newsall'),
    path('info/', views.info, name='info'),
]