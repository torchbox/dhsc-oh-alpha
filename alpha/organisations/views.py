from django.views.generic import FormView, TemplateView

from alpha.organisations import forms as organisation_forms


class AddVaccancies(TemplateView):
    template_name = "organisations/add_vacancies.html"

    def get(self, request, *args, **kwargs):
        self.request.session["organisation"] = {}
        return super().get(request, *args, **kwargs)


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
