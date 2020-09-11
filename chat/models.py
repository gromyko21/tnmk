from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Message(models.Model):
    author = models.ForeignKey(User, verbose_name="Отправитель", on_delete=models.CASCADE)
    recipient = models.ForeignKey(User, related_name='received_messages', verbose_name="Получатель", on_delete=models.CASCADE)
    message = models.TextField("Сообщение")
    pub_date = models.DateTimeField('Дата сообщения', default=timezone.now)
    is_readed = models.BooleanField('Прочитано', default=False)

    class Meta:
        verbose_name = u'Сообщение'
        verbose_name_plural = u'Сообщения'

    def __str__(self):
        return self.message
