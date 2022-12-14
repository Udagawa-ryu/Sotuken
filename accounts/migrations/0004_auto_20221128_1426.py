# Generated by Django 2.2.2 on 2022-11-28 05:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('maps', '0001_initial'),
        ('accounts', '0003_auto_20221128_1426'),
    ]

    operations = [
        migrations.AddField(
            model_name='mo6_visit_record',
            name='MO3_DspotNumber',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='maps.MO3_Default_spot', verbose_name='デフォルトスポットナンバー'),
        ),
        migrations.AddField(
            model_name='mo6_visit_record',
            name='MO4_OspotNumber',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='maps.MO4_Original_spot', verbose_name='オリジナルスポットナンバー'),
        ),
    ]
