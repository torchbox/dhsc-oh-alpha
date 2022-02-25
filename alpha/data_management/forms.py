from crispy_forms_gds.helper import FormHelper
from crispy_forms_gds.layout import HTML, Layout, Submit
from django import forms

from alpha.data_management import services


class DataUploadForm(forms.Form):
    file = forms.FileField(
        label="Upload a file",
        help_text="Select the CSV file to upload.",
        error_messages={"required": "Choose the CSV file you would like to import"},
    )

    def __init__(self, *args, **kwargs):
        super(DataUploadForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            HTML.heading("h1", "l", "Upload Ocupational Health Data"),
            "file",
            Submit("submit", "Submit"),
        )

    def clean_file(self):
        data = self.cleaned_data

        # TODO
        # This will force an error for the time being until we have use
        # cases planned out.
        services.parse_csv(data["file"])
        return data
