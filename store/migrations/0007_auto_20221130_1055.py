# Generated by Django 2.2.2 on 2022-11-30 01:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0006_remove_mo2_store_last_login'),
    ]

    operations = [
        migrations.AddField(
            model_name='mo2_store',
            name='MO2_images1',
            field=models.ImageField(blank=True, null=True, upload_to='store', verbose_name='店舗画像1'),
        ),
        migrations.AddField(
            model_name='mo2_store',
            name='MO2_images2',
            field=models.ImageField(blank=True, null=True, upload_to='store', verbose_name='店舗画像2'),
        ),
        migrations.AddField(
            model_name='mo2_store',
            name='MO2_images3',
            field=models.ImageField(blank=True, null=True, upload_to='store', verbose_name='店舗画像3'),
        ),
    ]
