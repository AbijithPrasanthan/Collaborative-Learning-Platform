from django.urls import path
from django.conf.urls import include
from CLP import views


urlpatterns = [
    path("login/", views.register, name="login"),
    path("home/", views.login_, name="home"),
    path("login/", views.user_logout, name="user_logout"),
]
