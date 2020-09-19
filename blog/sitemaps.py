from django.contrib.sitemaps import Sitemap
from .models import Post

class PostSitemap(Sitemap):
    changefreq = 'weekly' # частота обновления страниц
    priority = 0.9 # степень совпадения с тематикой сайта

    def items(self):
        return Post.published.all()
        # список объектов, отображ. на карте сайта
    def lastmod(self, obj):
        # возр время последней модификации статьи
        return obj.updated
