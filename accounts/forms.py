from .models import *
from django import forms
from django.contrib.auth.forms import UserCreationForm
from allauth.account.adapter import get_adapter
from allauth.account.forms import (
    SignupForm,
)

#クラス名はsettings.pyで書いた名前
class CustomSignupForm(UserCreationForm):
    # MO1_userName = forms.CharField(label='userName')
    # MO1_homeCountry = forms.CharField( label='homeCountry')
    # MO1_language = forms.CharField( label='language')
    # MO1_openRange =  forms.ChoiceField(choices = (
    #         (0, 'Open'),
    #         (1, 'Hidden'),
    #     ), label='openRange')
    class Meta:
        model = CustomUser
        fields = ["email","username","MO1_userID","MO1_homeCountry","MO1_language","MO1_openRange"]
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["email"].required = True
        labels = {
            "email": "mailAdress",
            "username":"UserName",
            "MO1_userID":"UserID",
            "MO1_homeCountry":"HomeCountry",
            "MO1_language":"Language",
            "MO1_openRange":"OpenRange",
        }
        # self.fields["email"].widget.attrs['class'] = 'form-control'
        # self.fields["email"].widget.attrs['placeholder'] = 'MailAdress'
        # self.fields['password1'].widget.attrs['class'] = 'form-control'
        # self.fields['password1'].widget.attrs['placeholder'] = 'password1'
        # self.fields['password2'].widget.attrs['class'] = 'form-control'
        # self.fields['password2'].widget.attrs['placeholder'] = 'password2'
        # self.fields['MO1_userName'].widget.attrs['class'] = 'form-control'
        # self.fields['MO1_userName'].widget.attrs['placeholder'] = 'MO1_userName'
        # self.fields['MO1_homeCountry'].widget.attrs['class'] = 'form-control'
        # self.fields['MO1_homeCountry'].widget.attrs['placeholder'] = 'MO1_homeCountry'
        # self.fields['MO1_language'].widget.attrs['class'] = 'form-control'
        # self.fields['MO1_language'].widget.attrs['placeholder'] = 'MO1_language'
        # self.fields['MO1_openRange'].widget.attrs['class'] = 'form-control'
        # self.fields['MO1_openRange'].widget.attrs['placeholder'] = 'MO1_openRange'
