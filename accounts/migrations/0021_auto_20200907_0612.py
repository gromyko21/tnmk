# Generated by Django 3.1 on 2020-09-07 03:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0020_auto_20200903_1013'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='image',
            field=models.FileField(blank=True, null=True, upload_to='image_post', verbose_name='Картинка'),
        ),
    ]
