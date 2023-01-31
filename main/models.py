from django.db import models
from django.utils import timezone
# Create your models here.

class MO11_Pointrecord(models.Model):
    MO11_pointRecordNumber = models.AutoField(verbose_name="ポイント履歴ナンバー",primary_key=True,editable=False)
    MO1_userNumber = models.ForeignKey("accounts.CustomUser", models.CASCADE, verbose_name="ユーザナンバー")
    MO2_storeNumber = models.ForeignKey("store.MO2_Store",models.CASCADE,verbose_name="使用店舗")
    MO11_pointSize= models.IntegerField(verbose_name="使用ポイント", default=0)
    MO11_createDate= models.DateTimeField(verbose_name="作成日時", default=timezone.now)

    def __str__(self):
        date = self.MO11_createDate.strftime("%Y/%m/%d")
        point = "「"+str(self.MO11_pointSize)+"」Point"
        return f'{self.MO1_userNumber}-{date}-{point}'