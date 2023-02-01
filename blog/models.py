from django.db import models
from django.utils import timezone
from accounts.models import *
# Create your models here.

def save_path1(instance, filename):
  ext = filename.split('.')[-1]
  f_name = "user_number_"+str(instance.MO1_userID.MO1_userNumber)
  t = instance.MO7_createDate.strftime("%Y/%m/%d/%H/%M/%S")
  time = t.replace('/', '-')
  return f'blog/{f_name}/{time}/1.{ext}'

def save_path2(instance, filename):
  ext = filename.split('.')[-1]
  f_name = "user_number_"+str(instance.MO1_userID.MO1_userNumber)
  t = instance.MO7_createDate.strftime("%Y/%m/%d/%H/%M/%S")
  time = t.replace('/', '-')
  return f'blog/{f_name}/{time}/2.{ext}'

def save_path3(instance, filename):
  ext = filename.split('.')[-1]
  f_name = "user_number_"+str(instance.MO1_userID.MO1_userNumber)
  t = instance.MO7_createDate.strftime("%Y/%m/%d/%H/%M/%S")
  time = t.replace('/', '-')
  return f'blog/{f_name}/{time}/3.{ext}'

# ブログモデル
class MO7_Blog(models.Model):
  MO7_blogNumber = models.AutoField(verbose_name="ブログナンバー",primary_key=True,editable=False)
  MO7_blogName = models.CharField(verbose_name="ブログ名", max_length=50)
  MO7_blogText = models.TextField(verbose_name="ブログ内容", null=True)
  MO7_blogImage1 = models.ImageField(upload_to=save_path1,null=True,blank=True)
  MO7_blogImage2 = models.ImageField(upload_to=save_path2,null=True,blank=True)
  MO7_blogImage3 = models.ImageField(upload_to=save_path3,null=True,blank=True)
  MO1_userID = models.ForeignKey("accounts.CustomUser", models.CASCADE, verbose_name="ユーザID")
  MO6_visitRecordNumber= models.ForeignKey("accounts.MO6_Visit_record", models.CASCADE, verbose_name="訪問記録ナンバー")
  MO7_openRange= models.IntegerField(verbose_name="公開範囲", default=0)
  MO7_createDate= models.DateTimeField(verbose_name="作成日時", default=timezone.now)
  MO7_updateDate= models.DateTimeField(verbose_name="更新日時", auto_now_add=True)

  class Meta:
    verbose_name_plural = "MO7_Blog"

  def __str__(self):
    date = self.MO7_createDate.strftime("%Y/%m/%d")
    return f'{date}-{self.MO7_blogName}'

#お気に入りブログモデル
class MO10_Fav_Blog(models.Model):
  MO1_userNumber = models.ForeignKey("accounts.CustomUser", models.CASCADE, verbose_name="ユーザナンバー")
  MO7_blogNumber = models.ForeignKey(MO7_Blog, models.CASCADE, verbose_name="ブログナンバー")

  class Meta:
    verbose_name_plural = "MO10_Fav_Blog"

  def __str__(self):
    return f'{self.MO1_userNumber}-{self.MO7_blogNumber.MO7_blogName}'