import re

from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import FormView, TemplateView

from alpha.organisations import forms as organisation_forms


class AddVaccancies(TemplateView):
    template_name = "organisations/add_vacancies.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["role_options"] = [
            ("role-1", "role 1"),
            ("role-2", "role 2"),
            ("role-3", "role 3"),
            ("role-4", "role 4"),
        ]
        return context

    def get_form_data(self):
        data = []
        post_data = dict(self.request.POST)

        roles = []
        numbers = []
        for i in post_data:
            if re.findall(r"role_", i):
                roles.append(post_data[i][0])
            if re.findall(r"number_", i):
                numbers.append(post_data[i][0])

        # make a template friendly list of the values submitted
        # EG [['role-2', '8'], ['role-3', '10']]
        for i, v in enumerate(roles):
            data.append([v, numbers[i]])

        return data

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)

        data = self.get_form_data()
        for i in data:
            try:
                int(i[1])
            except ValueError:
                context["error"] = True
                context["data"] = data
                return self.render_to_response(context)

        # Add vacancies to the sesion
        request.session["organisation"]["vacancies"] = data
        return redirect(reverse("organisations:sector"))


class StaffPerRole(AddVaccancies):
    template_name = "organisations/staff_per_role.html"

    def get(self, request, *args, **kwargs):
        self.request.session["organisation"] = {}
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)

        data = self.get_form_data()
        for i in data:
            try:
                int(i[1])
            except ValueError:
                context["error"] = True
                context["data"] = data
                return self.render_to_response(context)

        # Add employed_roles to the sesion
        request.session["organisation"]["employed_roles"] = data
        return redirect(reverse("organisations:add_vacancies"))


class Sector(FormView):
    template_name = "alpha/forms/generic_form.html"
    form_class = organisation_forms.SectorForm

    def form_valid(self, form):
        data = form.cleaned_data.copy()
        sector = organisation_forms.SECTORS[data["sectors"]]
        self.request.session["organisation"]["sector"] = sector
        return redirect(reverse("organisations:services"))


class Services(FormView):
    template_name = "alpha/forms/generic_form.html"
    form_class = organisation_forms.ServicesForm

    def form_valid(self, form):
        data = form.cleaned_data.copy()
        services = []
        for service in data["services"]:
            services.append(organisation_forms.SERVICES[service])

        self.request.session["organisation"]["services"] = services
        return redirect(reverse("organisations:regions"))


class Regions(FormView):
    template_name = "alpha/forms/generic_form.html"
    form_class = organisation_forms.RegionsForm

    def form_valid(self, form):
        data = form.cleaned_data.copy()
        regions = []
        for region in data["regions"]:
            regions.append(organisation_forms.REGIONS[region])

        self.request.session["organisation"]["regions"] = regions
        return redirect(reverse("organisations:review"))


class OrganisationDetailsReview(TemplateView):
    template_name = "organisations/review.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["organisation"] = self.request.session["organisation"]
        return context
