from django.urls import path

from alpha.home import views

urlpatterns = [
    path("", views.home, name="home"),
]
