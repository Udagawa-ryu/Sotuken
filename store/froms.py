from .models import *
from django import forms

class StoreCreateForm(forms.ModelForm):
    class Meta:
        model = MO2_store
        fields = ("MO2_storeName","MO2_storeInfo","MO2_phoneNumber","MO2_address","MO2_mailAdress","MO2_images1","MO2_images2","MO2_images3")
        labels = {
            "MO2_storeName":"店舗名(必須)",
            "MtO2_storeInfo":"店舗情報",
            "MO2_phoneNumber":"電話番号",
            "MO2_address":"住所(必須)",
            "MO2_mailAdress":"メールアドレス(必須)",
            "MO2_images1":"店舗画像1",
            "MO2_images2":"店舗画像2",
            "MO2_images3":"店舗画像3",
        }

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