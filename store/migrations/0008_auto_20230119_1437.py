# Generated by Django 2.2.2 on 2023-01-19 05:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0007_auto_20221130_1055'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mo2_store',
            name='MO2_images1',
            field=models.ImageField(blank=True, null=True, upload_to='store<django.db.models.fields.CharField>/', verbose_name='店舗画像1'),
        ),
        migrations.AlterField(
            model_name='mo2_store',
            name='MO2_images2',
            field=models.ImageField(blank=True, null=True, upload_to='store<django.db.models.fields.CharField>/', verbose_name='店舗画像2'),
        ),
        migrations.AlterField(
            model_name='mo2_store',
            name='MO2_images3',
            field=models.ImageField(blank=True, null=True, upload_to='store<django.db.models.fields.CharField>/', verbose_name='店舗画像3'),
        ),
    ]