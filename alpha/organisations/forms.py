from crispy_forms_gds.choices import Choice
from crispy_forms_gds.helper import FormHelper
from crispy_forms_gds.layout import HTML, Field, Layout, Size, Submit
from django import forms

SECTORS = {
    "nhs_oh": "NHS Trust Occupational Health service",
    "oh_private": "Occupational Health provider to private service",
    "embeded_non_nhs": "Occupational Health provider embedded within a non NHS public servivce (e.g military)",
    "embeded_private": "Occupational Health provider embedded within private organisation",
    "individual": "An individual worker (self employed)",
    "other": "Other (please specify)",
}

SERVICES = {
    "screening": "Screening services",
    "vaccines": "Vaccines and immunisation",
    "injury_rehabilitation": "Injury rehabilitation",
    "health_surveillance": "Health surveillance",
    "referrals_sickness": "Management referrals, sickness absence",
    "other": "Other (please specify)",
}

REGIONS = {
    "E": "Eastern",
    "EM": "East midlands",
    "L": "London",
    "NE": "North east",
    "NW": "North west",
    "SE": "South east",
    "SW": "South west",
    "WM": "West midlands",
    "YH": "Yorkshire and the Humber",
}


class SectorForm(forms.Form):
    SECTORS = (Choice(i, SECTORS[i]) for i in SECTORS)

    sectors = forms.ChoiceField(
        choices=SECTORS,
        widget=forms.RadioSelect,
        label="Which option best describes you or your organisation?",
        error_messages={"required": "Confirm your sector details."},
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.attrs = {"novalidate": 1}
        self.helper.layout = Layout(
            Field.checkboxes("sectors", legend_tag="h1", legend_size=Size.LARGE),
            Submit("submit", "Continue"),
        )


class ServicesForm(forms.Form):
    SERVICES = (Choice(i, SERVICES[i]) for i in SERVICES)

    services = forms.MultipleChoiceField(
        choices=SERVICES,
        widget=forms.CheckboxSelectMultiple,
        label="What occupational health services does your organisation provide?",
        error_messages={"required": "Select at least one service."},
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.attrs = {"novalidate": 1}
        self.helper.layout = Layout(
            HTML.p("Select all options that apply"),
            Field.checkboxes("services", legend_tag="h1", legend_size=Size.LARGE),
            Submit("submit", "Continue"),
        )


class RegionsForm(forms.Form):
    REGIONS = (Choice(i, REGIONS[i]) for i in REGIONS)

    regions = forms.MultipleChoiceField(
        choices=REGIONS,
        widget=forms.CheckboxSelectMultiple,
        label="Which regions does your organisation provide occupational health services in?",
        error_messages={"required": "Select at least one region."},
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.attrs = {"novalidate": 1}
        self.helper.layout = Layout(
            HTML.p("Select all options that apply"),
            Field.checkboxes("regions", legend_tag="h1", legend_size=Size.LARGE),
            Submit("submit", "Continue"),
        )
