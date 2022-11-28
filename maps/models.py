from django.db import models
from store.models import MO2_store
from accounts.models import CustomUser,MO6_Visit_record,MO8_Fav_Search_condition

# Create your models here.
# タグモデル
class MO5_Tag(models.Model):
  MO5_tagNumber = models.AutoField(verbose_name="タグナンバー",primary_key=True)
  MO5_tagName = models.CharField(verbose_name="タグ名")
  class Meta:
    verbose_name_plural = "MO5_Tag"

  def __str__(self):
    return self.MO5_tagNumber

# デフォルトスポットモデル
class MO3_Default_spot(models.Model):
  MO3_DspotNumber = models.AutoField(verbose_name="デフォルトスポットナンバー", primary_key=True)
  MO2_storeNumber = models.ForeignKey(MO2_store, models.CASCADE, verbose_name="ストアナンバー", editable=False)
  MO5_tagNumber = models.ForeignKey(MO5_Tag,models.CASCADE, verbose_name="タグナンバー")
  class Meta:
    verbose_name_plural = "MO3_Default_spot"

  def __str__(self):
    return self.MO3_DspotNumber

# オリジナルスポットモデル
class MO4_Original_spot(models.Model):
  MO4_OspotNumber = models.AutoField(verbose_name="オリジナルスポットナンバー", primary_key=True, null=True)
  MO4_OspotName = models.CharField(verbose_name="オリジナルスポット名",max_length=50, blank=True)
  MO4_OspotInfo = models.TextField(verbose_name="オリジナルスポット情報",null=True)
  MO4_OspotAdress = models.CharField(verbose_name="オリジナルスポット住所", max_length=50, null=True)
  MO4_createDate = models.DateTimeField(verbose_name="作成日時", auto_now_add=True)
  MO5_tagNumber = models.ForeignKey(MO5_Tag,models.CASCADE,verbose_name="タグナンバー" )
  MO1_userNumber = models.ForeignKey(CustomUser, models.CASCADE,verbose_name="ユーザナンバー")
  class Meta:
    verbose_name_plural = "MO4_Original_spot"

  def __str__(self):
    return self.MO4_OspotNumber

# お気に入り検索条件モデル
class MO8_Fav_Search_condition(models.Model):
  MO1_userNumber = models.ForeignKey(CustomUser, models.CASCADE, verbose_name="ユーザナンバー")
  MO5_tagNumber = models.ForeignKey(MO5_Tag,models.CASCADE, verbose_name="タグナンバー")
  class Meta:
    verbose_name_plural = "MO8_Fav_Search_condition"

  def __str__(self):
    return self.MO1_userNumber