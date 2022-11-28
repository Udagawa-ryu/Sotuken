from django.db import models
# from accounts.models import *
# Create your models here.

# ブログモデル
class MO7_Blog(models.Model):
  MO7_blogNumber = models.AutoField(verbose_name="ブログナンバー",primary_key=True,editable=False)
  MO7_blogName = models.CharField(verbose_name="ブログ名", max_length=50, blank=True)
  MO7_blogText = models.TextField(verbose_name="ブログ内容", null=True)
  MO1_userID = models.ForeignKey("accounts.CustomUser", models.CASCADE, verbose_name="ユーザID")
  MO6_visitRecordNumber= models.ForeignKey("accounts.MO6_Visit_record", models.CASCADE, verbose_name="訪問記録ナンバー")
  MO7_openRange= models.IntegerField(verbose_name="公開範囲", default=0)
  MO7_createDate= models.DateTimeField(verbose_name="作成日時", auto_now_add=True)
  MO7_updateDate= models.DateTimeField(verbose_name="更新日時", auto_now_add=True)

  class Meta:
    verbose_name_plural = "MO7_Blog"

  def __str__(self):
    return self.MO7_blogNumber

#お気に入りブログモデル
class MO10_Fav_Blog(models.Model):
  MO1_userNumber = models.ForeignKey("accounts.CustomUser", models.CASCADE, verbose_name="ユーザナンバー")
  MO7_blogNumber = models.ForeignKey(MO7_Blog, models.CASCADE, verbose_name="ブログナンバー")

  class Meta:
    verbose_name_plural = "MO10_Fav_Blog"

  def __str__(self):
    return self.MO1_userNumber