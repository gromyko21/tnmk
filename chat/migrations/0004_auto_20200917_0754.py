# Generated by Django 3.1 on 2020-09-17 04:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('chat', '0003_auto_20200916_1154'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chat',
            name='members',
            field=models.ManyToManyField(default=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL), related_name='members', to=settings.AUTH_USER_MODEL, verbose_name='Участник'),
        ),
        migrations.AlterField(
            model_name='message',
            name='timestamp',
            field=models.DateTimeField(auto_now=True, verbose_name='Дата сообщения'),
        ),
    ]