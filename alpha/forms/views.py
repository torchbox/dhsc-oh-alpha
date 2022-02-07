from django.conf import settings
from django.shortcuts import render
from django_gov_notify.message import NotifyEmailMessage

from alpha.forms.forms import ContactForm, TextInputForm


def signup(request):
    if request.method == "POST":
        form = TextInputForm(request.POST)
        if form.is_valid():
            pass

    else:
        form = TextInputForm()
    return render(request, "forms/signup.html", {"form": form})


def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form["name"].value()
            message = form["message"].value()
            email_address = form["email"].value()

            notify_message = NotifyEmailMessage(
                to=[email_address],
                template_id=settings.GOVUK_NOTIFY_PLAIN_EMAIL_TEMPLATE_ID,
                personalisation={
                    "name": name,
                    "message": message,
                },
            )
        notify_message.send()
    else:
        form = ContactForm()
    return render(request, "forms/contact.html", {"form": form})
