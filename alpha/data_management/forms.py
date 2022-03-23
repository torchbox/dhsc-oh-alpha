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
            HTML.heading("h1", "l", "Upload workforce data"),
            HTML.p(
                "Bulk upload demographic and employment data "
                "for all of your occupational health workforce in a single CSV file."
            ),
            HTML.heading("h2", "m", "Before you start"),
            HTML.p("You will need the following information for each member of staff:"),
            HTML.p(
                """<ul class="govuk-list govuk-list--bullet">
                        <li>name or unique reference ID</li>
                        <li>registered working location</li>
                        <li>role</li>
                        <li>professional identifier</li>
                        <li>hours usually worked per week</li>
                        <li>country of initial qualification</li>
                        <li>date of birth</li>
                        <li>employment start/end dates</li>
                    </ul>"""
            ),
            HTML.p(
                '<a href="/staff_data_eg.csv" class="govuk-button" aria-label="Download CSV">Download CSV</a>'
            ),
            "file",
            Submit("submit", "Submit"),
        )
