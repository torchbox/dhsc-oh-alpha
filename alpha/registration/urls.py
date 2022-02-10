from django.urls import path

from alpha.registration import views

app_name = "registration"

urlpatterns = [
    path(
        "preamble/",
        views.Preamble.as_view(),
        name="preamble",
    ),
    # select organisation branch
    path(
        "organisation_select_input/",
        views.OrganisationSelectInput.as_view(),
        name="organisation_select_input",
    ),
    path(
        "organisation_select_review/",
        views.OrganisationSelectReview.as_view(),
        name="organisation_select_review",
    ),
    path(
        "organisation_select_countries/",
        views.OrganisationSelectCountries.as_view(),
        name="organisation_select_countries",
    ),
    # create organisation branch
    path(
        "organisation_create_countries/",
        views.OrganisationCreateCountries.as_view(),
        name="organisation_create_countries",
    ),
    path(
        "organisation_create_postcode/",
        views.OrganisationCreatePostcode.as_view(),
        name="organisation_create_postcode",
    ),
    path(
        "organisation_create_address/",
        views.OrganisationCreateAddress.as_view(),
        name="organisation_create_address",
    ),
    path(
        "organisation_create_details/",
        views.OrganisationCreateDetails.as_view(),
        name="organisation_create_details",
    ),
    # end
    path(
        "person_details_input/",
        views.PersonDetailsInput.as_view(),
        name="person_details_input",
    ),
    path(
        "person_details_review/",
        views.PersonDetailsReview.as_view(),
        name="person_details_review",
    ),
    path(
        "not_eligible/",
        views.NotEligible.as_view(),
        name="not_eligible",
    ),
    path(
        "done/",
        views.Done.as_view(),
        name="done",
    ),
    path(
        "set_password/",
        views.SetPassword.as_view(),
        name="set_password",
    ),
]
