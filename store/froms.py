from .models import *
from django import forms

class StoreCreateForm(forms.ModelForm):
    class Meta:
        model = MO2_store
        fields = ("MO2_storeName","MO2_address","MO2_mailAdress")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['MO2_storeName'].widget.attrs['class'] = 'form-control'
        self.fields["MO2_storeName"].empty_label = '名称'
        self.fields['MO2_address'].widget.attrs['class'] = 'form-control'
        self.fields["MO2_address"].empty_label = '住所'
        self.fields['MO2_mailAdress'].widget.attrs['class'] = 'form-control'
        self.fields["MO2_mailAdress"].empty_label = 'メールアドレス'

class StorePassCreateForm(forms.Form):
    password1 = forms.CharField(label='パスワード1', widget=forms.PasswordInput(), min_length=8)
    password2 = forms.CharField(label='パスワード2', widget=forms.PasswordInput(), min_length=8)

class StoreLoginForm(forms.ModelForm):
    class Meta:
        model = MO2_store
        fields = ("MO2_mailAdress","MO2_password")
        labels = {
            "MO2_mailAdress": "MailAdress",
            "MO2_password":"Password",
        }
        widgets = {
            "MO2_password": forms.PasswordInput()
        }