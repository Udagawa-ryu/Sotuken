from .models import *
from accounts.models import *
from django import forms

class OspotCreateForm(forms.ModelForm):
    class Meta:
        model = MO4_Original_spot
        fields = ('MO1_userNumber','MO4_OspotName','MO4_OspotAdress')