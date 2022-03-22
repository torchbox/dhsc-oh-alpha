from crispy_forms_gds.helper import FormHelper
from crispy_forms_gds.layout import HTML, Layout, Submit
from django import forms

from alpha.data_management import services


class BulkDataUploadForm(forms.Form):
    file = forms.FileField(
        label="Upload a file",
        help_text="Select the CSV file to upload.",
        error_messages={"required": "Choose the CSV file you would like to import"},
    )

    def __init__(self, *args, **kwargs):
        super(BulkDataUploadForm, self).__init__(*args, **kwargs)
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


class BulkStaffDataUploadForm(BulkDataUploadForm):
    def __init__(self, *args, **kwargs):
        super(BulkStaffDataUploadForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            HTML.heading("h1", "l", "Add staff details in bulk"),
            HTML.p("Information you will need for each staff record"),
            HTML.p(
                """<ul class="govuk-list govuk-list--bullet">
                        <li>Name or unique reference ID</li>
                        <li>Registered working location</li>
                        <li>Role</li>
                        <li>Professional Identifier</li>
                        <li>Hours worked</li>
                        <li>Country of qualification</li>
                        <li>Date of birth</li>
                        <li>Employment start/end dates</li>
                    </ul>"""
            ),
            HTML.p(
                '<a href="/staff_data_eg.csv" class="govuk-button" aria-label="Download CSV">Download CSV</a>'
            ),
            "file",
            Submit("submit", "Submit"),
        )
