from django.urls import path

from alpha.data_management import views

app_name = "data_management"

urlpatterns = [
    path(
        "upload/",
        views.Upload.as_view(),
        name="upload",
    ),
    path(
        "success/",
        views.UpoadSuccess.as_view(),
        name="success",
    ),
]
