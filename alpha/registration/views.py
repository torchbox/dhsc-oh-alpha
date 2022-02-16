import base64
import json

from django.conf import settings
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
        providers = Provider.objects.all().values("name").order_by("name")
        context["providers"] = [provider["name"] for provider in providers]
        return context

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        provider = self.request.POST.get("input-autocomplete", None)

        try:
            # Have to search for the provider by name here
            provider = Provider.objects.get(name=provider)
        except Provider.DoesNotExist:
            # No provider, reload the search with a general error
            context["error"] = True
            return self.render_to_response(context)
        else:
            # Add provider to the session
            request.session["registration"]["selected_provider_id"] = provider.id
            return redirect(reverse("registration:organisation_select_review"))


class OrganisationSelectReview(FormView):
    template_name = "registration/organisation_select_review.html"
    form_class = registration_forms.ConfirmOrgDetailsForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["provider"] = get_provider_from_session(request=self.request)
        return context

    def form_valid(self, form):
        if form.cleaned_data["confirm"] == "no":
            return redirect(reverse("registration:organisation_select_input"))

        # If org is in England (from session):
        provider = get_provider_from_session(request=self.request)
        if provider and provider.covers_england:
            return redirect(reverse("registration:person_details_input"))
        else:
            # TODO - Can/Should we be redirecting back with messaging here?
            return redirect(reverse("registration:organisation_select_countries"))


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
        context["provider"] = get_provider_from_session(request=self.request)

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


def get_provider_from_session(request):
    registration = request.session.get("registration", None)
    if registration:
        provider_id = registration.get("selected_provider_id", None)
        if provider_id:
            return Provider.objects.get(id=provider_id)
