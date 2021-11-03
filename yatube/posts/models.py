from django.contrib.auth.models import User
from django.db import models


class Group(models.Model):
    title = models.CharField(
        max_length=200,
        verbose_name='Имя группы'
    )
    slug = models.SlugField(
        unique=True,
        verbose_name='Адрес'
    )
    description = models.TextField(
        verbose_name='Описание группы'
    )

    class Meta:
        ordering = ('-title', )
        verbose_name = 'группа'
        verbose_name_plural = 'группы'

    def __str__(self):
        return self.title


class Post(models.Model):
    text = models.TextField(
        verbose_name='Текст сообщения',
        help_text='Старайтесь писать корректно'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts',
        verbose_name='Автор'
    )
    group = models.ForeignKey(
        Group,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='posts',
        verbose_name='Группа',
        help_text='Группа, к которой будет относиться пост'
    )

    class Meta:
        ordering = ('-pub_date', )
        verbose_name = 'пост'
        verbose_name_plural = 'посты'

    def __str__(self):
        return self.text[:25]


class VotePost(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name='Голос за этот пост',
        related_name='posts'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Проголосовавший'
    )
