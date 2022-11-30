from django.db import models
from django import forms

# Create your models here.
class MO2_store(models.Model):
    MO2_storeNumber = models.AutoField(verbose_name="店舗ナンバー",primary_key=True, editable=False)
    MO2_storeName = models.CharField(verbose_name="店舗名",max_length=30)
    MO2_storeInfo = models.TextField(verbose_name="店舗情報",null=True,blank=True)
    MO2_phoneNumber = models.CharField(verbose_name="電話番号",null=True,max_length=20,blank=True)
    MO2_address = models.CharField(verbose_name="住所",max_length=50)
    MO2_mailAdress = models.EmailField(verbose_name="メールアドレス",unique=True)
    MO2_password = models.CharField(verbose_name="パスワード",null=True,max_length=255,blank=True)
    MO2_createDate = models.DateTimeField(verbose_name="作成日時", auto_now_add=True)
    MO2_updateDate = models.DateTimeField(verbose_name="更新日時", auto_now_add=True)
    MO2_images1 = models.ImageField(verbose_name="店舗画像1",upload_to="store",null=True,blank=True)
    MO2_images2 = models.ImageField(verbose_name="店舗画像2",upload_to="store",null=True,blank=True)
    MO2_images3 = models.ImageField(verbose_name="店舗画像3",upload_to="store",null=True,blank=True)
    is_active = models.BooleanField(verbose_name="is_active", default=False)
    is_auth = models.BooleanField(verbose_name="管理者認証",default=False)
    class Meta:
        verbose_name_plural = "MO2_Store"

    def __str__(self):
        return f'{self.MO2_storeNumber} - {self.MO2_storeName}'