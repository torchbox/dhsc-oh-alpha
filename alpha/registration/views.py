from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import FormView, TemplateView

from alpha.providers.models import Provider
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


class OrganisationSelectReview(FormView):
    template_name = "registration/organisation_select_review.html"
    form_class = registration_forms.ConfirmOrgDetailsForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        provider_id = 1  # TODO: get from session
        context["provider"] = Provider.objects.all().get(id=provider_id)
        return context

    def form_valid(self, form):
        if form.cleaned_data["confirm"] == "no":
            return redirect(reverse("registration:organisation_select_input"))

        # TODO: if org is in England (from session):
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


class OrganisationCreatePostcode(FormView):
    template_name = "registration/organisation_create_postcode.html"
    form_class = registration_forms.PostcodeForm

    def form_valid(self, form):
        return redirect(reverse("registration:organisation_create_address"))


class OrganisationCreateAddress(FormView):
    template_name = "registration/organisation_create_address.html"
    form_class = registration_forms.CreateAddressForm

    def form_valid(self, form):
        return redirect(reverse("registration:organisation_create_details"))


class OrganisationCreateDetails(FormView):
    template_name = "registration/organisation_create_details.html"
    form_class = registration_forms.AdditionalOrgDetailsForm

    def form_valid(self, form):
        return redirect(reverse("registration:person_details_input"))


class PersonDetailsInput(FormView):
    template_name = "registration/person_details_input.html"
    form_class = registration_forms.PersonDetailsForm

    def get_context_data(self, **kwargs):
        context = super(PersonDetailsInput, self).get_context_data(**kwargs)
        return context

    def form_valid(self, form):
        # return super(PersonDetailsInput, self).form_valid(form)
        # For now, forward the user
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


class SetPassword(FormView):
    template_name = "registration/set_password.html"
    form_class = registration_forms.SetPasswordForm

    def form_valid(self, form):
        return redirect(reverse("registration:TODO"))


class AccountCreated(TemplateView):
    template_name = "registration/account_created.html"
