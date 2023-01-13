from .models import *
from django import forms
from django.contrib.auth.forms import UserCreationForm
from allauth.account.adapter import get_adapter
from allauth.account.forms import (
    SignupForm,LoginForm
)

#クラス名はsettings.pyで書いた名前
class CustomSignupForm(UserCreationForm):
    COUNTRIES = {
        #どこかから国の一覧データを持ってきたい
        ("USA","USA"),
        ("日本","JAPAN"),
    }
    MO1_homeCountry = forms.ChoiceField(label="HomeCountry",choices=COUNTRIES)
    LANGAGES = {
        ("English","en"),
        ("日本語","ja"),
    }
    MO1_language = forms.ChoiceField(label="Language",choices=LANGAGES)
    MO1_openRange = forms.ChoiceField(label="OpenRange",choices={(0,"Open"),(1,"Hidden")})
    class Meta:
        model = CustomUser
        fields = ["email","username","MO1_userID","MO1_homeCountry","MO1_language","MO1_openRange"]
        labels = {
            "email": "mailAdress",
            "username":"UserName",
            "MO1_userID":"UserID",
            "MO1_homeCountry":"HomeCountry",
            "MO1_language":"Language",
            "MO1_openRange":"OpenRange",
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["email"].required = True
        self.fields['password1'].label = 'password'
        self.fields['password2'].label = 'password(confirmation)'

class CustomLoginForm(LoginForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            self.fields['login'].label = 'email'
            self.fields['password'].label = 'password'
            field.widget.attrs['class'] = 'form-control'

class UserEditForm(forms.ModelForm):
    COUNTRIES = {
        #どこかから国の一覧データを持ってきたい
        ("USA","USA"),
        ("日本","JAPAN"),
    }
    MO1_homeCountry = forms.ChoiceField(label="HomeCountry",choices=COUNTRIES)
    LANGAGES = {
        ("English","en"),
        ("日本語","ja"),
    }
    MO1_language = forms.ChoiceField(label="Language",choices=LANGAGES)
    MO1_openRange = forms.ChoiceField(label="OpenRange",choices={(0,"Open"),(1,"Hidden")})
    class Meta:
        model = CustomUser
        fields = ["username","MO1_userID","MO1_homeCountry","MO1_language","MO1_openRange"]
        labels = {
            "username":"UserName",
            "MO1_userID":"UserID",
            "MO1_homeCountry":"HomeCountry",
            "MO1_language":"Language",
            "MO1_openRange":"OpenRange",
        }

class UserSearchForm(forms.Form):
    s_user = forms.CharField(label="UserSearch")

class FavUserForm(forms.ModelForm):
    class Meta:
        model = MO9_Fav_Custom_user
        fields = ["MO1_userNumber","MO9_followedUserNumber"]