from .models import *
from accounts.models import *
from django import forms

class BlogRegisterForm(forms.ModelForm):
  MO6_visitRecordNumber = forms.ModelChoiceField(label="VisitRecord",queryset=MO6_Visit_record.objects.none())
  CHOICE = {
    (0,'OPEN'),
    (1,'HIDDEN'),
  }
  MO7_openRange = forms.ChoiceField(label='OpenRange', choices= CHOICE)
  class Meta:
    model = MO7_Blog
    # フォームに入力したいフィールドを選択
    fields = ('MO7_blogName','MO7_blogText','MO6_visitRecordNumber','MO7_openRange')
    # フォームのラベルの表示をフィールド名から任意の文字に変更
    labels = {
      'MO7_blogName':"BlogName",
      'MO7_blogText':"BlogText",
      'MO6_visitRecordNumber':'record',
      'MO7_openRange':'OpenRange',
    }
    # フォームの動きをモデルのフィールドとは違うものにしたいときに記述
    # widgets = {
    #   'MO7_openRange':forms.ChoiceField(label='OpenRange', widget=forms.RadioSelect, choices= CHOICE, initial=0)
    # }
  def __init__(self, *args, **kwargs):
    # self.user = kwargs.pop('user', None) #viewからのデータの受け取り
    super().__init__(*args, **kwargs)
