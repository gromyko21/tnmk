from django.db import models
from django.shortcuts import reverse
from django.utils.html import mark_safe
from django.contrib.auth.models import User
from slugify import slugify

class Article(models.Model):
    """
    Модель для создания новостей на главной странице
    """
    title = models.CharField(max_length=70, verbose_name='Название статьи')
    slug = models.SlugField(verbose_name="URL адрес статьи", unique=True, blank=True, null=True)
    text_article = models.TextField(max_length=5000, verbose_name='Содержание статьи')
    image = models.ImageField(upload_to='Articles', verbose_name='Главное изображение статьи')
    image_two = models.ImageField(upload_to='Articles', verbose_name='Дополнительное изображение')
    image_three = models.ImageField(upload_to='Articles', verbose_name='Дополнительное изображение')

    def image_tag(self):
        return mark_safe(u'<a href="{0}" target="_blank"><img src="{0}" width="150" height="130"/></a>'.format(self.image.url))

    def get_absolute_url(self):
        return reverse('articles_url', kwargs={'slug': self.slug})

    class Meta:
        verbose_name = u'Новость'
        verbose_name_plural = u'Новости'

    def __str__(self):
        return self.title

class Comment(models.Model):
    post = models.ForeignKey(Article, related_name='post',
                             on_delete=models.CASCADE,editable=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               verbose_name=u"Автор", related_name="author",editable=False)
    body = models.TextField(max_length=1000, verbose_name=u"Текст комментария")
    created = models.DateTimeField(auto_now_add=True, verbose_name=u"Дата создания")
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('created',)
        verbose_name = u'Коммертарий'
        verbose_name_plural = u'Комментарии'

    def __str__(self):
        return self.body
