from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import FormView, TemplateView

from alpha.data_management import forms as data_management_forms


class Upload(FormView):
    template_name = "alpha/forms/generic_form.html"
    form_class = data_management_forms.DataUploadForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def form_valid(self, form):
        return redirect(reverse("data_management:success"))


class UpoadSuccess(TemplateView):
    template_name = "data_management/upload_success.html"

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
