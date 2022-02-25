from django.urls import path

from alpha.dashboard import views

app_name = "dashboard"

urlpatterns = [
    path(
        "",
        views.Home.as_view(),
        name="home",
    )
]
