# Generated by Django 3.1 on 2020-10-22 06:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0010_readmessage'),
    ]

    operations = [
        migrations.AddField(
            model_name='readmessage',
            name='message_id',
            field=models.TextField(default=1, max_length=30, verbose_name='Id сообщения'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='readmessage',
            name='recipient',
            field=models.TextField(max_length=30, verbose_name='id получателей'),
        ),
        migrations.AlterField(
            model_name='readmessage',
            name='room_id',
            field=models.TextField(max_length=30, verbose_name='Id комнаты'),
        ),
    ]