from django.urls import path

from alpha.data_management import views

app_name = "data_management"

urlpatterns = [
    path(
        "upload_staff/",
        views.BulkUploadStaff.as_view(),
        name="bulk_upload_staff",
    ),
    path(
        "success/",
        views.UpoadSuccess.as_view(),
        name="success",
    ),
    path(
        "guide/",
        views.Guide.as_view(),
        name="guide",
    ),
]
