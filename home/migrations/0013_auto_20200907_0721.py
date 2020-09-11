# Generated by Django 3.1 on 2020-09-07 04:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0012_auto_20200903_1013'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='Articles', verbose_name='Главное изображение статьи'),
        ),
        migrations.AlterField(
            model_name='article',
            name='image_three',
            field=models.ImageField(blank=True, null=True, upload_to='Articles', verbose_name='Дополнительное изображение'),
        ),
        migrations.AlterField(
            model_name='article',
            name='image_two',
            field=models.ImageField(blank=True, null=True, upload_to='Articles', verbose_name='Дополнительное изображение'),
        ),
        migrations.AlterField(
            model_name='article',
            name='text_article',
            field=models.TextField(blank=True, max_length=5000, null=True, verbose_name='Содержание статьи'),
        ),
    ]