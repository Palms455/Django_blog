from django.db import models

from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from taggit.managers import TaggableManager
# менеджер тегов
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
    tags = TaggableManager()


    class Meta:
        ordering = ('-publish',)
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:post_detail', args=[self.publish.year,
                                                 self.publish.month, self.publish.day, self.slug])

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments', verbose_name='Пост')
    name = models.CharField(max_length=80, verbose_name='Заголовок комментария')
    email = models.EmailField()
    body = models.TextField(verbose_name='Тело комментария')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')
    active = models.BooleanField(default=True, verbose_name='Активное')

    class Meta:
        ordering = ('created',)
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return f'Комментарии {self.name} к посту {self.post}'
