from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import FormView, TemplateView

from alpha.data_management import forms as data_management_forms


class BulkUpload(FormView):
    template_name = "alpha/forms/generic_form.html"
    form_class = data_management_forms.BulkDataUploadForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def form_valid(self, form):
        return redirect(reverse("data_management:success"))


class BulkUploadStaff(BulkUpload):
    template_name = "data_management/upload_staff.html"
    form_class = data_management_forms.BulkStaffDataUploadForm
    pass


class UpoadSuccess(TemplateView):
    template_name = "data_management/upload_success.html"

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class Guide(TemplateView):
    template_name = "data_management/guide.html"
