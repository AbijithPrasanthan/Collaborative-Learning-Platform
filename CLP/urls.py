from django.conf.urls import include
from django.urls import path

from CLP import views

urlpatterns = [
    path("login/", views.register, name="login"),
    path("home/", views.login_, name="home"),
    path("login/", views.user_logout, name="user_logout"),
]
