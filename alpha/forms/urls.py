from django.urls import path

from alpha.forms import views

urlpatterns = [
    path("signup", views.signup, name="signup"),
    path("contact", views.contact, name="contact"),
]
