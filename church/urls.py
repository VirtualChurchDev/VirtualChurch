from django.urls import path
from . import views

app_name = "church"

urlpatterns = [
    path('', views.home, name='home'),
    path('pricing/', views.pricing, name='pricing'),
    path('newsall/', views.newsall, name='newsall'),
    path('info/', views.info, name='info'),
    path('browse/churches/', views.churchbrowser, name="churchbrowser"),
    path('church/<str:slug>', views.singlechurch, name="singlechurch"),
    path('church/<str:slug>/tour/', views.singlechurchtour, name="singlechurchtour"),
    path('browse/heads/', views.headbrowser, name="headbrowser"),
    path('head/<str:slug>', views.singlehead, name="singlehead"),
]