from django.urls import path

from alpha.organisations import views

app_name = "organisations"

urlpatterns = [
    path(
        "add_vacancies/",
        views.AddVaccancies.as_view(),
        name="add_vacancies",
    ),
    path(
        "staff_per_role/",
        views.StaffPerRole.as_view(),
        name="staff_per_role",
    ),
    path(
        "sector/",
        views.Sector.as_view(),
        name="sector",
    ),
    path(
        "services/",
        views.Services.as_view(),
        name="services",
    ),
    path(
        "regions/",
        views.Regions.as_view(),
        name="regions",
    ),
    path(
        "review/",
        views.OrganisationDetailsReview.as_view(),
        name="review",
    ),
]
