# Generated by Django 2.2.12 on 2020-08-31 04:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0016_auto_20200828_1034'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='profile',
        ),
    ]
