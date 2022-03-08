from crispy_forms_gds.choices import Choice
from crispy_forms_gds.helper import FormHelper
from crispy_forms_gds.layout import HTML, Field, Layout, Size, Submit
from django import forms


class SectorForm(forms.Form):
    SECTORS = (
        Choice("nhs_oh", "NHS Trust Occupational Health service"),
        Choice("oh_private", "Occupational Health provider to private service"),
        Choice(
            "embeded_non_nhs",
            "Occupational Health provider embedded within a non NHS public servivce (e.g military)",
        ),
        Choice(
            "embeded_private",
            "Occupational Health provider embedded within private organisation",
        ),
        Choice("individual", "An individual worker (self employed)"),
        Choice("other", "Other (please specify)"),
    )

    sectors = forms.ChoiceField(
        choices=SECTORS,
        widget=forms.RadioSelect,
        label="",
        error_messages={"required": "Confirm your sector details."},
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.attrs = {"novalidate": 1}
        self.helper.layout = Layout(
            HTML.heading(
                "h1", "l", "Which option best describes you or your organisation?"
            ),
            Field.checkboxes("sectors", legend_tag="h1", legend_size=Size.LARGE),
            Submit("submit", "Continue"),
        )


class ServicesForm(forms.Form):
    SERVICES = (
        Choice("screening", "Screening services"),
        Choice("vaccines", "Vaccines and immunisation"),
        Choice("injury_rehabilitation", "Injury rehabilitation"),
        Choice("health_surveillance", "Health surveillance"),
        Choice("referrals_sickness", "Management referrals, sickness absence"),
        Choice("other", "Other (please specify)"),
    )

    services = forms.MultipleChoiceField(
        choices=SERVICES,
        widget=forms.CheckboxSelectMultiple,
        label="",
        error_messages={"required": "Select at least one service."},
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.attrs = {"novalidate": 1}
        self.helper.layout = Layout(
            HTML.heading(
                "h1",
                "l",
                "What occupational health services does your organisation provide?",
            ),
            HTML.p("Select all options that apply"),
            Field.checkboxes("services", legend_tag="h1", legend_size=Size.LARGE),
            Submit("submit", "Continue"),
        )


class RegionsForm(forms.Form):
    REGIONS = (
        Choice("E", "Eastern"),
        Choice("EM", "East midlands"),
        Choice("L", "London"),
        Choice("NE", "North east"),
        Choice("NW", "North west"),
        Choice("SE", "South east"),
        Choice("SW", "South west"),
        Choice("WM", "West midlands"),
        Choice("YH", "Yorkshire and the Humber"),
    )

    regions = forms.MultipleChoiceField(
        choices=REGIONS,
        widget=forms.CheckboxSelectMultiple,
        label="",
        error_messages={"required": "Select at least one region."},
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.attrs = {"novalidate": 1}
        self.helper.layout = Layout(
            HTML.heading(
                "h1",
                "l",
                "Which regions does your organisation provide occupational health services in?",
            ),
            HTML.p("Select all options that apply"),
            Field.checkboxes("regions", legend_tag="h1", legend_size=Size.LARGE),
            Submit("submit", "Continue"),
        )
