from crispy_forms_gds.helper import FormHelper
from crispy_forms_gds.layout import Submit
from django import forms


class TextInputForm(forms.Form):

    name = forms.CharField(
        label="Name",
        help_text="Your full name.",
        widget=forms.TextInput(),
        error_messages={"required": "Enter your name as it appears on your passport"},
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit("submit", "Submit"))


class ContactForm(forms.Form):

    name = forms.CharField(
        label="Name",
        help_text="Your full name.",
        widget=forms.TextInput(),
        error_messages={"required": "Enter your name as it appears on your passport"},
    )
    message = forms.CharField(
        label="Message",
        help_text="Your message",
        widget=forms.TextInput(),
        error_messages={"required": "Please type a message"},
    )
    email = forms.CharField(
        label="Email",
        help_text="Your Email address",
        widget=forms.EmailInput(),
        error_messages={"required": "Please add your email"},
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit("submit", "Submit"))
