from django.db import models
from django import forms
from accounts.models import CustomUser,MO6_Visit_record

# Create your models here.

# ブログモデル
class MO7_Blog(models.Model):
  MO7_blogNumber = models.AutoField(verbose_name="ブログナンバー",primary_key=True,editable=False)
  MO7_blogName = models.CharField(verbose_name="ブログ名", max_length=50, blank=True)
  MO7_blogText = models.TextField(verbose_name="ブログ内容", null=True)
  MO1_userID = models.ForeignKey(CustomUser,on_delete=models.CASCADE, verbose_name="ユーザID")
  MO6_visitRecordNumber= models.ForeignKey(MO6_Visit_record, on_delete=models.CASCADE, verbose_name="訪問記録ナンバー")
  MO7_openRange= models.IntegerField(verbose_name="公開範囲", default=0)
  MO7_createDate= models.DateTimeField(verbose_name="作成日時", auto_now_add=True)
  MO7_updateDate= models.DateTimeField(verbose_name="更新日時", auto_now_add=True)

#お気に入りブログモデル
class MO10_Fav_Blog(models.Model):
  MO1_userNumber = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name="ユーザナンバー")
  MO7_blogNumber = models.ForeignKey(MO7_Blog, on_delete=models.CASCADE, verbose_name="ブログナンバー")