from django.urls import path
from . import views

app_name = "chat"

urlpatterns = [
    path('', views.index, name='index'),
    path('join/', views.join, name='join'),
    path('create/', views.create, name='create'),
    path('payment/', views.payment, name='payment'),
    path('send/', views.sendChat, name='send'),
    path('mksuper/', views.mksuper, name='mksuper'),
    path('<str:room_name>/', views.room, name='room'),
]
