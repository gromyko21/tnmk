# Generated by Django 3.1 on 2020-09-24 04:25

from django.conf import settings
import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Chat',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('group_name', models.CharField(max_length=50)),
                ('image_chat', models.ImageField(blank=True, null=True, upload_to='image_chat', verbose_name='Фото беседы')),
                ('creater', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('members', models.ManyToManyField(default=django.contrib.auth.models.User, related_name='members', to=settings.AUTH_USER_MODEL, verbose_name='Участник')),
            ],
        ),
        migrations.CreateModel(
            name='ReadMessage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('read', models.BooleanField(default=False, verbose_name='Прочитано')),
                ('recipient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='chat.chat', verbose_name='Получатель')),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(verbose_name='Сообщение')),
                ('image_message', models.ImageField(blank=True, null=True, upload_to='message_image', verbose_name='Изображения в сообщениях')),
                ('file_message', models.ImageField(blank=True, null=True, upload_to='message_file')),
                ('timestamp', models.DateTimeField(auto_now=True, verbose_name='Дата сообщения')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Отправитель')),
                ('is_readed', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='chat.readmessage', verbose_name='Прочитано')),
                ('recipient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='received_messages', to='chat.chat', verbose_name='Получатель')),
            ],
            options={
                'verbose_name': 'Сообщение',
                'verbose_name_plural': 'Сообщения',
            },
        ),
    ]
