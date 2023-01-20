# Generated by Django 2.2.2 on 2023-01-20 00:43

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_mo6_visit_record_mo6_createddate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='MO1_userID',
            field=models.CharField(max_length=32, unique=True, validators=[django.core.validators.MinLengthValidator(7)], verbose_name='UserID'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='username',
            field=models.CharField(max_length=50, verbose_name='UserName'),
        ),
    ]