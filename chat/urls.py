from django.urls import path
from . import views

app_name = "chat"

urlpatterns = [
    path('', views.index, name='index'),
    path('join/<str:room_number>', views.join, name='join'),
    path('complete/<str:room_number>', views.complete, name='complete'),
    path('delete/<str:room_number>', views.delete, name='delete'),
    path('create/', views.create, name='create'),
    path('payment/', views.payment, name='payment'),
    path('send/', views.sendChat, name='send'),
    path('<str:room_name>/', views.room, name='room'),
]
