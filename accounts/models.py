from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.shortcuts import reverse
from django.utils.html import mark_safe
from slugify import slugify


class Profile(models.Model):
    """
    Модель для личного профиля для пользователей
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30, verbose_name='Имя', default='Новый')
    last_name = models.CharField(max_length=30, verbose_name='Фамилия', default='Пользователь')
    slug = models.SlugField(verbose_name="URL адрес", unique=True, blank=True, null=True, default='{}')
    bio = models.TextField(max_length=500, blank=True, verbose_name='Информация о человеке')
    birth_date = models.DateField(null=True, blank=True, verbose_name='Дата рождения')
    image = models.ImageField(null=True, blank=True, upload_to="image_profil", verbose_name='Фото профиля', default='default_photo')

    def image_tag(self):
        return mark_safe(u'<a href="{0}" target="_blank"><img src="{0}" width="150" height="130"/></a>'.format(self.image.url))


    def get_absolute_url(self):
        return reverse('user_url', kwargs={'slug': self.slug})

    class Meta:
        verbose_name = u'Пользователя'
        verbose_name_plural = u'Пользователи'

    def __str__(self):
        return self.first_name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.user.username)
        return super(Profile, self).save(*args, **kwargs)

#Обновление модели автоматически сохраняется
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

class Post(models.Model):
    datetime = models.DateTimeField(verbose_name=u"Дата", auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=u"Автор", related_name="posts")
    text = models.CharField(max_length=1000, verbose_name=u"Текст", null=True, blank=True)
    image = models.FileField(verbose_name=u"Картинка", null=True, blank=True, default='default_photo')

    def __str__(self):
        return self.text

    class Meta:
        ordering = ["-datetime"]
        verbose_name = u'Пользовательскую новость'
        verbose_name_plural = u'Пользовательские новости'

    def image_tag(self):
        return mark_safe(u'<a href="{0}" target="_blank"><img src="{0}" width="150" height="130"/></a>'.format(self.image.url))
