# Generated by Django 2.2.2 on 2023-01-25 00:47

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0009_auto_20230120_1437'),
    ]

    operations = [
        migrations.AddField(
            model_name='mo6_visit_record',
            name='MO6_visitDate',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='訪問日時'),
        ),
    ]
