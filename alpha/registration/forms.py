from crispy_forms_gds.choices import Choice
from crispy_forms_gds.helper import FormHelper
from crispy_forms_gds.layout import Field, Layout, Size, Submit
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
