from django.shortcuts import render

from alpha.forms.forms import TextInputForm


def signup(request):
    if request.method == "POST":
        form = TextInputForm(request.POST)
        if form.is_valid():
            pass

    else:
        form = TextInputForm()
    return render(request, "forms/signup.html", {"form": form})
