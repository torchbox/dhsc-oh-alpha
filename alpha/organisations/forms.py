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
        Choice("other", "Other (please specify"),
    )

    sectors = forms.ChoiceField(
        choices=SECTORS,
        widget=forms.RadioSelect,
        label="",
        error_messages={"required": "Select at least one sector."},
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
