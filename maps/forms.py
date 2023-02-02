from .models import *
from accounts.models import *
from django import forms

class OspotCreateForm(forms.ModelForm):
    MO4_OspotName = forms.CharField(max_length=50,required=True)
    class Meta:
        model = MO4_Original_spot
        fields = ('MO1_userNumber','MO4_OspotName','MO4_OspotInfo','MO4_OspotLat','MO4_OspotLng')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

class SpotSearchForm(forms.Form):
    words = forms.CharField(label="keyword",max_length=40)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

