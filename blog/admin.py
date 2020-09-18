from django.contrib import admin
from .models import Post, Comment
# Register your models here.

#admin.site.register(Post)

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'author', 'publish', 'status') # Отображение
    list_filter = ('status', 'created', 'publish', 'author') # Блок фильтрации списка
    search_fields = ('title', 'body') # поиск по полям
    prepopulated_fields = {'slug': ('title',)} # автоматическое генерирование слага на основе titlr
    raw_id_fields = ('author',) # поиск по полю автор
    date_hierarchy = 'publish' # навигаия по датам
    ordering = ('status', 'publish') # сортировка по

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'post', 'created', 'active')
    list_filter = ('active', 'created', 'updated')
    search_fields = ('name', 'email', 'body')
