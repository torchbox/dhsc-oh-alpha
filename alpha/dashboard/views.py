from django.views.generic import TemplateView


class Home(TemplateView):
    template_name = "dashboard/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["organisation"] = "Occupational Health For All"
        context["user"] = {"name": "Sam", "email": "sam@ohforall.com"}

        # Control showing a different include in the template if the url
        # has dashboard/?org_data=True
        org_data = self.request.GET.get("org_data", "")
        if org_data:
            context["organisation_data"] = True

        return context
