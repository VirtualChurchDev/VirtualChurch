from django.urls import path
from . import views

app_name = "account"

urlpatterns = [
    path('login_user', views.login_user, name='login_user'),
    path('logout_user', views.logout_user, name='logout_user'),
    path('register_user', views.register_user, name='register_user'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('headpanel', views.headpanel, name='headpanel'),
    path('activate/<uidb64>/<token>', views.activate, name='activate'),
    path('password_change', views.password_change, name='password_change'),
    path('password_recover', views.password_recover, name='password_recover'),
    path('recovery/<uidb64>/<token>', views.recovery, name='recovery'),
]