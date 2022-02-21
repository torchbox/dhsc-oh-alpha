import re

from crispy_forms_gds.choices import Choice
from crispy_forms_gds.helper import FormHelper
from crispy_forms_gds.layout import HTML, Field, Fieldset, Layout, Size, Submit
from django import forms
from django.core.exceptions import ValidationError
from django.shortcuts import reverse


class ConfirmOrgDetailsForm(forms.Form):
    confirm = forms.ChoiceField(
        choices=(("yes", "Yes"), ("no", "No, search again")),
        widget=forms.RadioSelect,
        label="Are these details correct?",
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.attrs = {"novalidate": 1}
        self.helper.layout = Layout(
            Field.radios(
                "confirm", legend_size=Size.MEDIUM, legend_tag="h1", inline=True
            ),
            Submit("submit", "Continue"),
        )


class CountriesForm(forms.Form):
    COUNTRIES = (
        Choice("E", "England"),
        Choice("S", "Scotland"),
        Choice("W", "Wales"),
        Choice("NI", "Northern Ireland"),
    )

    countries = forms.MultipleChoiceField(
        choices=COUNTRIES,
        widget=forms.CheckboxSelectMultiple,
        label="",
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.attrs = {"novalidate": 1}
        self.helper.layout = Layout(
            HTML.heading("h1", "l", "Where does your organisation provide services?"),
            HTML.p("Select all that apply"),
            Field.checkboxes("countries", legend_tag="h1", legend_size=Size.LARGE),
            Submit("submit", "Continue"),
        )


class PersonDetailsForm(forms.Form):

    full_name = forms.CharField(
        label="Full name",
        widget=forms.TextInput(),
        error_messages={"required": "Enter your name as it appears on your passport"},
    )

    job_title = forms.CharField(
        label="Job title (optional)",
        widget=forms.TextInput(),
        error_messages={"required": "Please add your job title"},
        required=False,
    )

    email = forms.CharField(
        label="Email address",
        help_text="Try to avoid shared email addresses like admin@myworkplace.com",
        widget=forms.EmailInput(),
        error_messages={"required": "Please add your email"},
    )

    phone_number = forms.CharField(
        label="Phone number (optional)",
        help_text="We will only use this if we are unable to contact you by email to verify your organisation.",
        required=False,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit("submit", "Continue"))
        self.helper.attrs = {"novalidate": 1}
        self.helper.layout = Layout(
            HTML.heading("h1", "l", "Enter your user details"),
            Fieldset(
                Field.text("full_name"),
                Field.text("email"),
                Field.text("job_title"),
                Field.text("phone_number"),
                legend="We will use these details if we need to contact you about your organisation.",
            ),
        )


class PostcodeForm(forms.Form):
    postcode = forms.CharField(
        label="Enter a postcode",
        error_messages={"required": "A postcode is required"},
    )

    def clean_postcode(self):
        data = self.cleaned_data
        data["postcode"] = re.sub("[^A-Z0-9]", "", str(data["postcode"]).upper())

        if data["postcode"] == "SE64AF":
            return data

        raise ValidationError(
            "No Addresses Found with postcode: %(postcode)s",
            params={"postcode": data["postcode"]},
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.attrs = {"novalidate": 1}
        self.helper.layout = Layout(
            HTML.heading("h1", "l", "Find your organisation's address"),
            Fieldset(
                Field.text("postcode"),
                legend="We'll use your postcode to find the address.",
            ),
            Submit("submit", "Find address"),
        )


class CreateAddressForm(forms.Form):

    address = forms.ChoiceField(
        choices=(
            ("", "10 addresses found"),
            (1, "1 Richmond Road SE6 4AF"),
            (2, "2 Richmond Road SE6 4AF"),
            (3, "3 Richmond Road SE6 4AF"),
            (4, "4 Richmond Road SE6 4AF"),
            (5, "5 Richmond Road SE6 4AF"),
            (6, "6 Richmond Road SE6 4AF"),
            (7, "7 Richmond Road SE6 4AF"),
            (8, "8 Richmond Road SE6 4AF"),
            (9, "9 Richmond Road SE6 4AF"),
            (10, "10 Richmond Road SE6 4AF"),
        ),
        label="",
    )

    def __init__(self, *args, **kwargs):
        super(CreateAddressForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.attrs = {"novalidate": 1}
        self.helper.layout = Layout(
            HTML.heading("h1", "l", "Select your organisation"),
            HTML(
                '<div class="govuk-grid-row">'
                '<div class="govuk-grid-column-one-half">'
                "<p>Postcode entered: <strong>SE6 4AF</strong></p>"
                "</div>"
                '<div class="govuk-grid-column-one-half">'
                '<p><a class="govuk-link" href="'
                + reverse("registration:organisation_create_postcode")
                + '">Change</a></p>'
                "</div>"
                "</div>"
            ),
            "address",
            HTML.p(
                '<a class="govuk-link" href="#">Organisation address is not listed or is not correct</a>'
            ),
            Submit("submit", "Continue"),
        )


class AdditionalOrgDetailsForm(forms.Form):

    website = forms.CharField(
        label="Website (optional)", widget=forms.TextInput(), required=False
    )
    email = forms.CharField(
        label="Main organisation email address",
        help_text="This should be a shared email like admin@myworkplace.com",
        widget=forms.EmailInput(),
        error_messages={"required": "Please add your email"},
    )

    phone_number = forms.CharField(
        label="Phone number (optional)",
        help_text="We will only use this if we are unable to contact you by email to verify your organisation.",
        required=False,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit("submit", "Continue"))
        self.helper.attrs = {"novalidate": 1}
        self.helper.layout = Layout(
            HTML.heading("h1", "l", "Enter your organisation’s contact details"),
            Fieldset(
                Field.text("email"),
                Field.text("website"),
                Field.text("phone_number"),
                legend="We will use these details to verify that your organisation is an occupational health provider.",
            ),
        )


class SetPasswordForm(forms.Form):
    password = forms.CharField(
        label="Password",
        help_text="Minimum 8 characters in length with at least one number and one letter",
        widget=forms.PasswordInput(),
    )
    confirm = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(),
    )

    def clean_password(self):
        data = self.cleaned_data
        MIN_LENGTH = 8

        if len(data["password"]) < MIN_LENGTH:
            raise forms.ValidationError(
                "Password must be at least %d characters long." % MIN_LENGTH
            )

        if not re.search(r"[0-9]", data["password"]) or not re.search(
            r"[A-Z]", data["password"], re.IGNORECASE
        ):
            raise forms.ValidationError(
                "Password must be at contain at least one number and one letter"
            )

        return data["password"]

    def clean(self):
        data = super().clean()
        if data.get("password") != data.get("confirm"):
            raise ValidationError("Passwords do not match")
        return data

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.attrs = {"novalidate": 1}
        self.helper.layout = Layout(
            HTML.heading("h1", "l", "Create a password"),
            HTML.p(
                "Complete your registration by creating a secure and memorable password."
            ),
            HTML.p("Associated email: <strong>{{email}}</strong>"),
            Fieldset(
                Field.text("password"),
                Field.text("confirm"),
            ),
            Submit("submit", "Continue"),
        )
