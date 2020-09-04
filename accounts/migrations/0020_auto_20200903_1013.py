# Generated by Django 3.1 on 2020-09-03 07:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('accounts', '0019_auto_20200901_0924'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='profile',
            options={'verbose_name': 'Данные пользователя', 'verbose_name_plural': 'Данные пользователей'},
        ),
        migrations.AlterField(
            model_name='post',
            name='image',
            field=models.FileField(blank=True, default='default_photo', null=True, upload_to='image_post', verbose_name='Картинка'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='user',
            field=models.OneToOneField(editable=False, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]