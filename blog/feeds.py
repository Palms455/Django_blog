from django.contrib.syndication.views import Feed
from django.template.defaultfilters import truncatewords
from .models import Post
# автоматическая генерация RSS

class LatestPostsFeed(Feed):
    title = 'My blog'
    link = '/blog/'
    description = 'Новые посты блога.'

    def items(self):
        # объекты в рассылку
        return Post.published.all()[:5]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return truncatewords(item.body, 30)
