# Generated by Django 2.2.2 on 2022-11-29 03:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_auto_20221126_0913'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mo2_store',
            name='MO2_password',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='パスワード'),
        ),
    ]
