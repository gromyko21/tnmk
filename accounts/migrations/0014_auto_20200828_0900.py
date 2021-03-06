# Generated by Django 2.2.12 on 2020-08-28 06:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0013_post_profile'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='position',
            field=models.CharField(default='Должность сотрудника', max_length=100, verbose_name='Должность'),
        ),
        migrations.AlterField(
            model_name='post',
            name='profile',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='profiles', to='accounts.Profile', verbose_name='Профиль пользователя'),
        ),
    ]
