# Generated by Django 2.2.2 on 2023-01-24 11:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('maps', '0004_auto_20230124_1948'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mo4_original_spot',
            name='MO4_OspotLat',
            field=models.DecimalField(decimal_places=28, max_digits=32, null=True, verbose_name='オリジナルスポットY座標'),
        ),
        migrations.AlterField(
            model_name='mo4_original_spot',
            name='MO4_OspotLng',
            field=models.DecimalField(decimal_places=28, max_digits=32, null=True, verbose_name='オリジナルスポットY座標'),
        ),
    ]