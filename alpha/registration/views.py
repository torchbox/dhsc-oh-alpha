from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import FormView, TemplateView

from alpha.registration import forms as registration_forms


class Preamble(TemplateView):
    template_name = "registration/preamble.html"

    def get(self, request, *args, **kwargs):
        self.request.session.clear()
        self.request.session["registration"] = {}
        return super().get(request, *args, **kwargs)


class OrganisationSelectInput(TemplateView):
    template_name = "registration/organisation_select_input.html"

    def post(self, request, *args, **kwargs):
        # TODO: if "can't find":
        # return redirect(reverse("registration:organisation_create_countries"))
        # else:
        return redirect(reverse("registration:organisation_select_review"))


class OrganisationSelectReview(TemplateView):
    template_name = "registration/organisation_select_review.html"

    def post(self, request, *args, **kwargs):
        # TODO: if org is in England:
        return redirect(reverse("registration:person_details_input"))
        # else:
        # return redirect(reverse("registration:organisation_select_countries"))


class OrganisationSelectCountries(FormView):
    template_name = "registration/countries.html"
    form_class = registration_forms.CountriesForm

    def form_valid(self, form):
        if "E" not in form.cleaned_data["countries"]:
            return redirect(reverse("registration:not_eligible"))
        return redirect(reverse("registration:organisation_select_review"))


class OrganisationCreateCountries(FormView):
    template_name = "registration/countries.html"
    form_class = registration_forms.CountriesForm

    def form_valid(self, form):
        if "E" not in form.cleaned_data["countries"]:
            return redirect(reverse("registration:not_eligible"))
        return redirect(reverse("registration:organisation_create_postcode"))


class OrganisationCreatePostcode(TemplateView):
    template_name = "registration/organisation_create_postcode.html"

    def post(self, request, *args, **kwargs):
        return redirect(reverse("registration:organisation_create_address"))


class OrganisationCreateAddress(TemplateView):
    template_name = "registration/organisation_create_address.html"

    def post(self, request, *args, **kwargs):
        return redirect(reverse("registration:organisation_create_details"))


class OrganisationCreateDetails(TemplateView):
    template_name = "registration/organisation_create_details.html"

    def post(self, request, *args, **kwargs):
        return redirect(reverse("registration:person_details_input"))


class PersonDetailsInput(TemplateView):
    template_name = "registration/person_details_input.html"

    def post(self, request, *args, **kwargs):
        return redirect(reverse("registration:person_details_review"))


class PersonDetailsReview(TemplateView):
    template_name = "registration/person_details_review.html"

    def post(self, request, *args, **kwargs):
        return redirect(reverse("registration:done"))


class NotEligible(TemplateView):
    template_name = "registration/not_eligible.html"


class Done(TemplateView):
    template_name = "registration/done.html"

    def get(self, request, *args, **kwargs):
        resp = super().get(request, *args, **kwargs)
        self.request.session["registration"] = {}
        return resp
