from django.db import models
from django.shortcuts import reverse
from django.utils.html import mark_safe
from django.contrib.auth.models import User


class Article(models.Model):
    """
    Модель для создания новостей на главной странице
    """
    title = models.CharField(max_length=70, verbose_name='Название статьи')
    slug = models.SlugField(verbose_name="URL адрес статьи", unique=True, blank=True, null=True)
    text_article = models.TextField(max_length=5000, verbose_name='Содержание статьи', blank=True, null=True)
    image = models.ImageField(upload_to='Articles', verbose_name='Главное изображение статьи', blank=True, null=True)
    image_two = models.ImageField(upload_to='Articles', verbose_name='Дополнительное изображение', blank=True, null=True)
    image_three = models.ImageField(upload_to='Articles', verbose_name='Дополнительное изображение', blank=True, null=True)

    #def image_tag(self):
        #return mark_safe(u'<a href="{0}" target="_blank"><img src="{0}" width="150" height="130"/></a>'.format(self.image.url))

    def get_absolute_url(self):
        return reverse('articles_url', kwargs={'slug': self.slug})

    class Meta:
        verbose_name = u'Новость'
        verbose_name_plural = u'Новости'

    def __str__(self):
        return self.title


class Comment(models.Model):
    '''
    Комментарии к записям на главной странице
    '''
    post = models.ForeignKey(Article, related_name='post',
                             on_delete=models.CASCADE, editable=False)
    author = models.OneToOneField(User, on_delete=models.CASCADE,
                               verbose_name=u"Автор", related_name="author", editable=False)
    body = models.TextField(max_length=1000, verbose_name=u"Текст комментария")
    created = models.DateTimeField(auto_now_add=True, verbose_name=u"Дата создания")
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('created',)
        verbose_name = u'Коммертарий'
        verbose_name_plural = u'Комментарии'

    def __str__(self):
        return self.body


class Question(models.Model):
    """
    Вопрос для опроса
    """
    article_id = models.OneToOneField(Article, on_delete=models.CASCADE, related_name='r_article')
    title = models.CharField(max_length=200, verbose_name="Вопрос")
    date_published = models.DateTimeField(verbose_name="Дата публикации", auto_now_add=True)
    is_active = models.BooleanField(verbose_name="Опубликован")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Опрос'
        verbose_name_plural = 'Опросы'


class Answer(models.Model):
    """
    Вариант ответа на вопрос
    """
    question_id = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='r_question')
    answer = models.CharField(max_length=200, verbose_name="Ответ")
    votes = models.IntegerField(verbose_name="Голосов", default=0)

    def __str__(self):
        return self.answer

    class Meta:
        verbose_name = 'Ответ'
        verbose_name_plural = 'Ответы'


class AnswerUser(models.Model):
    """
    Ответы пользователей
    """
    answer_id = models.OneToOneField(Answer, on_delete=models.CASCADE, related_name='r_question')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='r_user')

    # def __str__(self):
    #     return self.answer_id

    class Meta:
        verbose_name = 'Ответ'
        verbose_name_plural = 'Ответы'
