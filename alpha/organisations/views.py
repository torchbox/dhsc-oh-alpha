from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import FormView, TemplateView

from alpha.organisations import forms as organisation_forms


class AddVaccancies(TemplateView):
    template_name = "organisations/add_vacancies.html"

    def get(self, request, *args, **kwargs):
        # This will be set in a simalr way to the preamble so will shift from here
        self.request.session["organisation"] = {}
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        # Get values here and store in session by lazily organizing the post data
        data = []
        roles = self.request.POST.getlist("role")
        numbers = self.request.POST.getlist("number")
        for i, v in enumerate(roles):
            data.append([v, numbers[i]])
        # Add roles to the seesion
        request.session["organisation"]["roles"] = data
        # Just reload this view so we can see it's worked
        return redirect(reverse("organisations:after_vacancies"))


# Just prove this is sticking
class AfterVaccancies(TemplateView):
    template_name = "organisations/after_vacancies.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            context["roles"] = self.request.session["organisation"]["roles"]
        except KeyError:
            pass
        return context


class StaffPerRole(TemplateView):
    template_name = "organisations/staff_per_role.html"

    def get(self, request, *args, **kwargs):
        self.request.session["organisation"] = {}
        return super().get(request, *args, **kwargs)


class Sector(FormView):
    template_name = "alpha/forms/generic_form.html"
    form_class = organisation_forms.SectorForm


class Services(FormView):
    template_name = "alpha/forms/generic_form.html"
    form_class = organisation_forms.ServicesForm


class Regions(FormView):
    template_name = "alpha/forms/generic_form.html"
    form_class = organisation_forms.RegionsForm


class OrganisationDetailsReview(TemplateView):
    template_name = "organisations/review.html"
