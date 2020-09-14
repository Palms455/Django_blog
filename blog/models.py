from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
# Create your models here.


class PublishedManager(models.Manager):
    """Кастомный models manager"""
    def get_queryset(self):
        return super().get_queryset().filter(status='published')

class Post(models.Model):

    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published')
    )
    title = models.CharField(max_length=250, verbose_name='Заголовок поста')
    slug = models.SlugField(max_length=250, unique_for_date='publish')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts', verbose_name='Автор')
    body = models.TextField(verbose_name='Тело поста')
    publish = models.DateTimeField(default=timezone.now(), verbose_name='Дата публикации')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft', verbose_name='Статус публикации')

    objects = models.Manager() # Менеджер по умолчанию
    published = PublishedManager() # Кастомный менеджер


    class Meta:
        ordering = ('-publish',)
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'

    def __str__(self):
        return self.title
