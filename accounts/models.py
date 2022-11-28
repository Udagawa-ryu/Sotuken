from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.core.mail import send_mail
from django.utils import timezone
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils.translation import gettext_lazy as _

# # Create your models here.
# class UserManager(BaseUserManager):
#     use_in_migrations = True
#     def _create_user(self, email,password, **extra_fields):
#         if not email:
#             raise ValueError('Emailを入力して下さい')
#         email = self.normalize_email(email)
#         user = self.model(email=email, **extra_fields)
#         user.set_password(password)
#         user.save(using=self.db)
#         return user
#     def create_user(self, email, password=None, **extra_fields):
#         extra_fields.setdefault('is_staff', False)
#         extra_fields.setdefault('is_superuser', False)
#         return self._create_user(email, password, **extra_fields)
#     def create_superuser(self,email, password="admin", **extra_fields):
#         extra_fields.setdefault('is_staff', True)
#         extra_fields.setdefault('is_superuser', True)
#         if extra_fields.get('is_staff') is not True:
#             raise ValueError('is_staff=Trueである必要があります。')
#         if extra_fields.get('is_superuser') is not True:
#             raise ValueError('is_superuser=Trueである必要があります。')
#         return self._create_user(email, password, **extra_fields)
# class CustomUser(AbstractBaseUser,PermissionsMixin):
#     MO1_userNumber = models.AutoField(verbose_name="ユーザナンバー",primary_key=True, editable=False)
#     MO1_userID = models.CharField(verbose_name="ユーザID",max_length=16)
#     MO1_userName = models.CharField(verbose_name="ユーザ名",max_length=50,blank=True)
#     email = models.EmailField(verbose_name="メールアドレス",unique=True)
#     MO1_homeCountry = models.CharField(verbose_name="所在国",max_length=50,blank=True)
#     MO1_language = models.CharField(verbose_name="使用言語",max_length=50,blank=True)
#     MO1_openRange = models.IntegerField(verbose_name="公開範囲",default=0)
#     MO1_point = models.IntegerField(verbose_name="ポイント",default=0)
#     MO1_createDate = models.DateTimeField(verbose_name="作成日時", auto_now_add=True)
#     MO1_updateDate = models.DateTimeField(verbose_name="更新日時", auto_now_add=True)
#     is_staff = models.BooleanField(_("staff status"), default=False)
#     is_active = models.BooleanField(_("active"), default=True)

#     objects = UserManager()
#     USERNAME_FIELD = "email"
#     EMAIL_FIELD = "email"
#     REQUIRED_FIELDS = ["MO1_userName"]
#     USER_MODEL_EMAIL_FIELD = "email"
#     class Meta:
#         verbose_name_plural = _('Customuser')
#     def clean(self):
#         super().clean()
#         self.email = self.__class__.objects.normalize_email(self.email)
#     def email_user(self, subject, message, from_email=None, **kwargs):
#         send_mail(subject, message, from_email, [self.email], **kwargs)

class CustomUser(AbstractUser):
    MO1_userNumber = models.AutoField(verbose_name="ユーザナンバー",primary_key=True, editable=False)
    MO1_userID = models.CharField(verbose_name="ユーザID",max_length=16)
    username = models.CharField(verbose_name="ユーザ名",max_length=50,blank=True)
    email = models.EmailField(verbose_name="メールアドレス",unique=True)
    MO1_homeCountry = models.CharField(verbose_name="所在国",max_length=50,blank=True)
    MO1_language = models.CharField(verbose_name="使用言語",max_length=50,blank=True)
    MO1_openRange = models.IntegerField(verbose_name="公開範囲",default=0)
    MO1_point = models.IntegerField(verbose_name="ポイント",default=0)
    MO1_createDate = models.DateTimeField(verbose_name="作成日時", auto_now_add=True)
    MO1_updateDate = models.DateTimeField(verbose_name="更新日時", auto_now_add=True)
    is_staff = models.BooleanField(_("staff status"), default=False)
    is_active = models.BooleanField(_("active"), default=True)
    REQUIRED_FIELDS = ["username","MO1_userID","MO1_homeCountry","MO1_language","MO1_openRange"]
    USERNAME_FIELD = "email"
    EMAIL_FIELD = "email"
    class Meta:
        verbose_name_plural = "CustomUser"

    def __str__(self):
        return self.MO1_userID

class MO6_Visit_record(models.Model):
    MO6_visitRecordNumber = models.AutoField(verbose_name="訪問記録ナンバー", primary_key=True, editable=False)
    MO1_userNumber = models.ForeignKey(CustomUser, models.CASCADE, verbose_name="ユーザナンバー")
    MO6_dateofvisit = models.DateTimeField(verbose_name="訪問記録", auto_now_add=True)
    MO3_DspotNumber = models.ForeignKey("maps.MO3_Default_spot", models.CASCADE, verbose_name="デフォルトスポットナンバー")
    MO4_OspotNumber = models.ForeignKey("maps.MO4_Original_spot", models.CASCADE, verbose_name="オリジナルスポットナンバー")
    class Meta:
        verbose_name_plural = "MO6_Visit_record"

    def __str__(self):
        return self.MO1_userNumber

class MO9_Fav_Custom_user(models.Model):
    MO1_userNumber = models.ForeignKey(CustomUser, models.CASCADE, verbose_name="ユーザナンバー",related_name='myuser')
    MO9_followedUserNumber = models.ForeignKey(CustomUser, models.CASCADE, verbose_name="フォローユーザナンバー",related_name='followeduser')
    class Meta:
        verbose_name_plural = "MO9_Fav_Custom_user"

    def __str__(self):
        return self.MO1_userNumber