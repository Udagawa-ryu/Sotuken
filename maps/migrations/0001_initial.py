# Generated by Django 2.2.2 on 2022-11-28 05:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('store', '0003_auto_20221126_0913'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='MO5_Tag',
            fields=[
                ('MO5_tagNumber', models.AutoField(editable=False, primary_key=True, serialize=False, verbose_name='タグナンバー')),
                ('MO5_tagName', models.CharField(max_length=50, verbose_name='タグ名')),
            ],
            options={
                'verbose_name_plural': 'MO5_Tag',
            },
        ),
        migrations.CreateModel(
            name='MO8_Fav_Search_condition',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('MO1_userNumber', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='ユーザナンバー')),
                ('MO5_tagNumber', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='maps.MO5_Tag', verbose_name='タグナンバー')),
            ],
            options={
                'verbose_name_plural': 'MO8_Fav_Search_condition',
            },
        ),
        migrations.CreateModel(
            name='MO4_Original_spot',
            fields=[
                ('MO4_OspotNumber', models.AutoField(editable=False, primary_key=True, serialize=False, verbose_name='オリジナルスポットナンバー')),
                ('MO4_OspotName', models.CharField(blank=True, max_length=50, verbose_name='オリジナルスポット名')),
                ('MO4_OspotInfo', models.TextField(null=True, verbose_name='オリジナルスポット情報')),
                ('MO4_OspotAdress', models.CharField(max_length=50, null=True, verbose_name='オリジナルスポット住所')),
                ('MO4_createDate', models.DateTimeField(auto_now_add=True, verbose_name='作成日時')),
                ('MO1_userNumber', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='ユーザナンバー')),
                ('MO5_tagNumber', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='maps.MO5_Tag', verbose_name='タグナンバー')),
            ],
            options={
                'verbose_name_plural': 'MO4_Original_spot',
            },
        ),
        migrations.CreateModel(
            name='MO3_Default_spot',
            fields=[
                ('MO3_DspotNumber', models.AutoField(editable=False, primary_key=True, serialize=False, verbose_name='デフォルトスポットナンバー')),
                ('MO2_storeNumber', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.MO2_store', verbose_name='ストアナンバー')),
                ('MO5_tagNumber', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='maps.MO5_Tag', verbose_name='タグナンバー')),
            ],
            options={
                'verbose_name_plural': 'MO3_Default_spot',
            },
        ),
    ]