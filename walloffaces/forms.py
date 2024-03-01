from django import forms
from bootstrap_datepicker_plus import DatePickerInput
from django_recaptcha.fields import ReCaptchaField
from django_recaptcha.widgets import ReCaptchaV3


from .models import Veteran, Remembrance


class BioForm(forms.ModelForm):
    class Meta:
        model = Veteran
        fields = ("name", "hometown", "county", "dob", "doc", "branch",
                  "rank", "status", "country", "image", "bio", "adtl_img_1",
                  "adtl_img_2", "adtl_img_3", "adtl_img_4", "adtl_img_5",
                  "adtl_img_6")
        widgets = {
            "dob": DatePickerInput(format="%m/%d/%Y"),
            "doc": DatePickerInput(format="%m/%d/%Y"),
        }


class BioFormAdmin(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(BioFormAdmin, self).__init__(*args, **kwargs)
        self.fields['bio'].widget.attrs['class'] = 'tiny-class'

    class Meta:
        model = Veteran
        fields = ("name", "hometown", "county", "dob", "doc", "branch",
                  "rank", "status", "country", "image", "bio", "adtl_img_1",
                  "adtl_img_2", "adtl_img_3", "adtl_img_4", "adtl_img_5",
                  "adtl_img_6", "approved")


class DonateForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    phone = forms.CharField(max_length=11, label="Phone Number")
    amount = forms.IntegerField()


class RemembranceForm(forms.ModelForm):
    veteran = forms.ModelChoiceField(
        queryset=Veteran.objects.all(), widget=forms.HiddenInput()
    )
    validator = forms.CharField(max_length=40,
                                required=True, label="2 + 3 =", help_text="Please prove that you're human")

    class Meta:
        model = Remembrance
        fields = ("veteran", "title", "remembrance",
                  "name", "email", "relationship")

class ContactForm(forms.Form):
    name = forms.CharField(max_length=100) 
    email = forms.EmailField()
    subject = forms.CharField(max_length=100) 
    message = forms.CharField(widget=forms.Textarea) 
    captcha = ReCaptchaField(widget=ReCaptchaV3) 