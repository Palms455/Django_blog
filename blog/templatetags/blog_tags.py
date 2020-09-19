from django import template
from ..models import Post
from django.db.models import Count

register = template.Library()
# для регистрации пользовательских тегов

# по умлч название функции исп. в кач. названия тега
# задать имя тега @register.simple_tag(name='my_tag')
@register.simple_tag
def total_posts():
    return Post.published.count()

@register.inclusion_tag('blog/post/latest_posts.html')
# регистрация тега и указания шаблона, где будет применятся
def show_latest_posts(count=5):
    # Для задания count в шаблоне нужено {% show_latest_posts 3 %}
    lat_posts = Post.published.order_by('-publish')[:count]
    return {'latest_posts': lat_posts}

@register.simple_tag
def get_most_commented_posts(count=5):
    return Post.published.annotate(total_comments=Count('comments')).order_by('-total_comments')[:count]

