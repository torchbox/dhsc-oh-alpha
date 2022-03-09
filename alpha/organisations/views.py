import re

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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["role_options"] = [
            ("role-1", "role 1"),
            ("role-2", "role 2"),
            ("role-3", "role 3"),
            ("role-4", "role 4"),
        ]
        return context

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)

        # Get values here and store in session by lazily organizing the post data
        data = []
        post_data = dict(self.request.POST)

        roles = []
        numbers = []
        for i in post_data:
            if re.findall(r"role_", i):
                roles.append(post_data[i])
            if re.findall(r"number_", i):
                numbers.append(post_data[i])

        # make a template friendly list of the values submitted
        for i, v in enumerate(roles):
            data.append([v, numbers[i]])

        # Number validation
        for i in data:
            try:
                int(i[1][0])
            except ValueError:
                context["error"] = True
                context["data"] = data
                return self.render_to_response(context)

        # Add roles to the sesion
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
