from django import forms
from bootstrap_datepicker_plus import DatePickerInput

from .models import Veteran


class BioForm(forms.ModelForm):
    class Meta:
        model = Veteran
        fields = ("name", "hometown", "county", "dob", "doc", "branch",
                  "rank", "status", "country", "image", "bio")
        widgets = {
            "dob": DatePickerInput(format="%m/%d/%Y"),
            "doc": DatePickerInput(format="%m/%d/%Y"),
        }


class DonateForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    phone = forms.CharField(max_length=11, label="Phone Number")
    amount = forms.IntegerField()
