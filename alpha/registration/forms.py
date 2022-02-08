from crispy_forms_gds.choices import Choice
from crispy_forms_gds.helper import FormHelper
from crispy_forms_gds.layout import Field, Fieldset, Layout, Size, Submit
from django import forms


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
        label="Where does your organisation provide services?",
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field.checkboxes("countries", legend_size=Size.LARGE),
            Submit("submit", "Continue"),
        )


class PersonDetailsForm(forms.Form):

    full_name = forms.CharField(
        label="Full name",
        widget=forms.TextInput(),
        error_messages={"required": "Enter your name as it appears on your passport"},
    )

    job_title = forms.CharField(
        label="Job title",
        widget=forms.TextInput(),
        error_messages={"required": "Please add your job title"},
    )

    email = forms.CharField(
        label="Email address",
        help_text="Try to avoid shared email addresses like admin@myworkplace.com",
        widget=forms.EmailInput(),
        error_messages={"required": "Please add your email"},
    )

    phone_number = forms.CharField(
        label="Phone number",
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit("submit", "Continue"))
        self.helper.attrs = {"novalidate": 1}
        self.helper.layout = Layout(
            Fieldset(
                Field.text("full_name"),
                Field.text("job_title"),
                Field.text("email"),
                Field.text("phone_number"),
                legend="We will use these details to contact you about your organisation",
            )
        )