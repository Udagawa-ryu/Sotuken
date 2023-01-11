from .models import *
from django import forms

# class FavoriteBlogListForm(forms.ModelForm):
#   class Meta:
#     model = 

class PointForm(forms.Form):
  point = forms.IntegerField(label="point")