import base64
import json

from django.conf import settings
from django.core import serializers
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import FormView, TemplateView
from django_gov_notify.message import NotifyEmailMessage

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

    def get_context_data(self, **kwargs):
        context = super(OrganisationSelectInput, self).get_context_data(**kwargs)
        providers = list(Provider.objects.all().values("name"))
        list_of_providers = []
        for provider in providers:
            list_of_providers.append(provider["name"])
        context["providers"] = list_of_providers
        return context


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
        self.request.session["registration"]["person"] = form.cleaned_data.copy()

        # return super(PersonDetailsInput, self).form_valid(form)
        # For now, forward the user
        return redirect(reverse("registration:person_details_review"))


class PersonDetailsReview(TemplateView):
    template_name = "registration/person_details_review.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        provider_id = 1  # TODO: get from session
        context["provider"] = Provider.objects.all().get(id=provider_id)

        context["person"] = self.request.session["registration"]["person"]
        return context


class NotEligible(TemplateView):
    template_name = "registration/not_eligible.html"


class Done(TemplateView):
    template_name = "registration/done.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["email"] = self.request.session["registration"]["person"]["email"]
        return context

    def get(self, request, *args, **kwargs):
        TEMPLATE_ID = "306cb1b6-7a53-47ad-809d-a678cdaa3ea5"
        email_address = self.request.session["registration"]["person"]["email"]
        ref_num = "HDJ2123F"
        password_link = self.request.build_absolute_uri(
            reverse(
                "registration:set_password",
                args=(encode_email(email_address),),
            )
        )

        if settings.GOVUK_NOTIFY_API_KEY:
            notify_message = NotifyEmailMessage(
                to=[email_address],
                template_id=TEMPLATE_ID,
                personalisation={
                    "ref_num": ref_num,
                    "password_link": password_link,
                },
            )
            notify_message.send()
        else:
            print("email vars:")
            print(
                json.dumps(
                    {
                        "template_id": TEMPLATE_ID,
                        "email_address": email_address,
                        "ref_num": ref_num,
                        "password_link": password_link,
                    },
                    indent=2,
                )
            )

        resp = super().get(request, *args, **kwargs)
        self.request.session["registration"] = {}
        return resp


class SetPassword(FormView):
    template_name = "registration/set_password.html"
    form_class = registration_forms.SetPasswordForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["email"] = decode_email(self.kwargs["email"])
        return context

    def form_valid(self, form):
        return redirect(reverse("registration:TODO"))


class AccountCreated(TemplateView):
    template_name = "registration/account_created.html"


def encode_email(email):
    return base64.urlsafe_b64encode(email.encode("utf-8")).decode("ascii")


def decode_email(b64):
    return base64.urlsafe_b64decode(b64).decode("utf-8")
