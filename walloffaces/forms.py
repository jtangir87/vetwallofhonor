from django import forms
from bootstrap_datepicker_plus import DatePickerInput

from .models import Veteran, Remembrance


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


class RemembranceForm(forms.ModelForm):
    veteran = forms.ModelChoiceField(
        queryset=Veteran.objects.all(), widget=forms.HiddenInput()
    )

    class Meta:
        model = Remembrance
        fields = ("veteran", "title", "remembrance",
                  "name", "email", "relationship")
