# Generated by Django 2.2.12 on 2020-08-20 07:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_auto_20200820_0616'),
    ]

    operations = [
        migrations.AlterField(
            model_name='articles',
            name='slug',
            field=models.SlugField(blank=True, null=True, unique=True, verbose_name='Slug'),
        ),
    ]
