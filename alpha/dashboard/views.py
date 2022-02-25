from django.views.generic import TemplateView


class Home(TemplateView):
    template_name = "dashboard/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["organisation"] = "Occupational Health For All"
        context["user"] = {"name": "Sam", "email": "sam@ohforall.com"}
        return context
