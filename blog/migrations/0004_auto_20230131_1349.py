# Generated by Django 2.2.2 on 2023-01-31 04:49

import blog.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_mo7_blog_mo7_blogimage1'),
    ]

    operations = [
        migrations.AddField(
            model_name='mo7_blog',
            name='MO7_blogImage2',
            field=models.ImageField(blank=True, null=True, upload_to=blog.models.save_path2),
        ),
        migrations.AddField(
            model_name='mo7_blog',
            name='MO7_blogImage3',
            field=models.ImageField(blank=True, null=True, upload_to=blog.models.save_path3),
        ),
        migrations.AlterField(
            model_name='mo7_blog',
            name='MO7_blogImage1',
            field=models.ImageField(blank=True, null=True, upload_to=blog.models.save_path1),
        ),
    ]
