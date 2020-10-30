from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import reverse


class Chat(models.Model):
    group_name = models.CharField(max_length=50)
    creater = models.ForeignKey(User, on_delete=models.CASCADE)
    members = models.ManyToManyField(User, verbose_name="Участник", related_name='members', default=User)
    image_chat = models.ImageField(null=True, blank=True, upload_to="image_chat", verbose_name='Фото беседы')

    def __str__(self):
        return self.group_name

    def get_absolute_url(self):
        return reverse('private_chat_url', kwargs={'id': self.id})


class ReadMessage(models.Model):
    room_id = models.TextField('Id комнаты', max_length=30)
    message_id = models.TextField('Id сообщения', max_length=30)
    recipient = models.TextField('id получателей', max_length=30)
    is_read = models.BooleanField('Прочитано', default=False)


class Message(models.Model):
    author = models.ForeignKey(User, verbose_name="Отправитель", on_delete=models.CASCADE)
    recipient = models.ForeignKey(Chat, related_name='received_messages', verbose_name="Получатель", on_delete=models.CASCADE)
    content = models.TextField("Сообщение", default='Нет сообщения', max_length=2000)
    image = models.TextField("Фотографии", blank=True, null=True)
    file = models.TextField("Файл", blank=True, null=True)
    timestamp = models.DateTimeField('Дата сообщения', auto_now_add=True)
    is_readed = models.BooleanField('Прочитано', default=False)

    class Meta:
        verbose_name = u'Сообщение'
        verbose_name_plural = u'Сообщения'

    def __str__(self):
        return self.content
