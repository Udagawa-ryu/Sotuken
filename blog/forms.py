from .models import *
from accounts.models import *
from django import forms

class ImageWidget(forms.widgets.ClearableFileInput):
    template_name = "catalog/widgets/image_widget.html"
class BlogRegisterForm(forms.ModelForm):
  MO6_visitRecordNumber = forms.ModelChoiceField(label="VisitRecord",queryset=MO6_Visit_record.objects.none())
  CHOICE = {
    (0,'publish to the public'),
    (1,'private'),
  }
  MO7_openRange = forms.ChoiceField(label='OpenRange', choices= CHOICE)
  class Meta:
    model = MO7_Blog
    # フォームに入力したいフィールドを選択
    fields = ('MO1_userID','MO7_blogName','MO7_blogText','MO7_blogImage1','MO7_blogImage2','MO7_blogImage3','MO6_visitRecordNumber','MO7_openRange')
    # フォームのラベルの表示をフィールド名から任意の文字に変更
    labels = {
      'MO7_blogName':"BlogName",
      'MO7_blogText':"BlogText",
      'MO7_blogImage1':'BlogImage1',
      'MO7_blogImage2':'BlogImage2',
      'MO7_blogImage3':'BlogImage3',
      'MO6_visitRecordNumber':'record',
      'MO7_openRange':'OpenRange',
    }
    widgets = {"MO7_blogImage1": ImageWidget}
    # フォームの動きをモデルのフィールドとは違うものにしたいときに記述
    # widgets = {
    #   'MO7_openRange':forms.ChoiceField(label='OpenRange', widget=forms.RadioSelect, choices= CHOICE, initial=0)
    # }
