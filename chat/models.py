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


# class ReadMessage(models.Model):
#     read = models.BooleanField('Прочитано', default=False)
#     recipient = models.ForeignKey(Chat, verbose_name="Получатель", on_delete=models.CASCADE)


class Message(models.Model):
    author = models.ForeignKey(User, verbose_name="Отправитель", on_delete=models.CASCADE)
    recipient = models.ForeignKey(Chat, related_name='received_messages', verbose_name="Получатель", on_delete=models.CASCADE)
    content = models.TextField("Сообщение", default='Нет сообщения')
    image_message = models.ImageField(null=True, blank=True, upload_to="message_image", verbose_name='Изображения в сообщениях')
    image_message2 = models.ImageField(null=True, blank=True, upload_to="message_image", verbose_name='Изображения в сообщениях')
    image_message3 = models.ImageField(null=True, blank=True, upload_to="message_image", verbose_name='Изображения в сообщениях')
    image_message4 = models.ImageField(null=True, blank=True, upload_to="message_image", verbose_name='Изображения в сообщениях')
    image_message5 = models.ImageField(null=True, blank=True, upload_to="message_image", verbose_name='Изображения в сообщениях')
    file_message = models.FileField(null=True, blank=True, upload_to="message_file")
    file_message2 = models.FileField(null=True, blank=True, upload_to="message_file")
    file_message3 = models.FileField(null=True, blank=True, upload_to="message_file")
    timestamp = models.DateTimeField('Дата сообщения', auto_now_add=True)
    is_readed = models.BooleanField('Прочитано', default=False)

    class Meta:
        verbose_name = u'Сообщение'
        verbose_name_plural = u'Сообщения'

    def __str__(self):
        return self.content
