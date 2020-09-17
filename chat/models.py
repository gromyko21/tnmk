from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import reverse
from slugify import slugify


class Chat(models.Model ):
    group_name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, unique=True)
    creater = models.ForeignKey(User, on_delete=models.CASCADE)
    members = models.ManyToManyField(User, verbose_name="Участник", related_name='members')

    def __str__(self):
        return self.slug

    def get_absolute_url(self):
        return reverse('private_chat_url', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        self.slug = slugify(self.group_name)
        return super(Chat, self).save(*args, **kwargs)



class Message(models.Model):
    author = models.ForeignKey(User, verbose_name="Отправитель", on_delete=models.CASCADE)
    recipient = models.ForeignKey(Chat, related_name='received_messages', verbose_name="Получатель", on_delete=models.CASCADE)
    content = models.TextField("Сообщение")
    timestamp = models.DateTimeField('Дата сообщения', auto_now=True)
    is_readed = models.BooleanField('Прочитано', default=False)

    class Meta:
        verbose_name = u'Сообщение'
        verbose_name_plural = u'Сообщения'

    def __str__(self):
        return self.content
