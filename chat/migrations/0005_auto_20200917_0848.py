# Generated by Django 3.1 on 2020-09-17 05:48

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('chat', '0004_auto_20200917_0754'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chat',
            name='members',
            field=models.ManyToManyField(related_name='members', to=settings.AUTH_USER_MODEL, verbose_name='Участник'),
        ),
    ]