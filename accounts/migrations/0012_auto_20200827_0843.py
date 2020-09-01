# Generated by Django 2.2.12 on 2020-08-27 05:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0011_auto_20200826_0658'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='post',
            options={'ordering': ['-datetime'], 'verbose_name': 'Пользовательскую новость', 'verbose_name_plural': 'Пользовательские новости'},
        ),
        migrations.AlterModelOptions(
            name='profile',
            options={'verbose_name': 'Пользователя', 'verbose_name_plural': 'Пользователи'},
        ),
        migrations.AlterField(
            model_name='post',
            name='image',
            field=models.FileField(blank=True, default='default_photo', null=True, upload_to='', verbose_name='Картинка'),
        ),
    ]