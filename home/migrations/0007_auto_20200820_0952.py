# Generated by Django 2.2.12 on 2020-08-20 09:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0006_auto_20200820_0950'),
    ]

    operations = [
        migrations.RenameField(
            model_name='article',
            old_name='Второе изображение',
            new_name='image',
        ),
        migrations.RenameField(
            model_name='article',
            old_name='Главное изображение',
            new_name='image_three',
        ),
        migrations.RenameField(
            model_name='article',
            old_name='Третье изображение',
            new_name='image_two',
        ),
    ]
