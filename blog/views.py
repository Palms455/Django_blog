from django.shortcuts import render, get_object_or_404
from .models import Post, Comment
from django.db.models import Count
# функция аггрегации + Avg - сред, Max, Min
from taggit.models import Tag
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from .forms import EmailPostForm, CommentForm, SearchForm
from django.core.mail import send_mail
from django.contrib.postgres.search import SearchVector


# Create your views here.

def post_list(request, tag_slug=None):
    obj_list = Post.published.all()
    tag = None
    if tag_slug:
        # вывод постов по тегам
        tag = get_object_or_404(Tag, slug=tag_slug)
        obj_list = obj_list.filter(tags__in=[tag])
    paginator = Paginator(obj_list, 3) #разбивка по кол-ву статей на странице
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    return render(request, 'blog/post/list.html', {'page': page, 'posts': posts, 'tag': tag})

class PosrListView(ListView):
    queryset = Post.published.all()  # или model = Post
    context_object_name = 'posts'  # без указания - objects_list
    paginate_by = 3
    template_name = 'blog/post/list.html'


def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post, status='published', publish__year=year,
                             publish__month=month, publish__day=day)
    # активные комментарии поста
    comments = post.comments.filter(active=True)
    new_comment = None
    if request.method == 'POST':
        # отправка пользователем коммента
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            # создание коммента до загрузки в бд
            new_comment = comment_form.save(commit=False)
            # привязка коммента к посту
            new_comment.post = post
            # сохранение в бд
            new_comment.save()
    else:
        comment_form = CommentForm()

    # Формирование списка похожих статей.
    post_tags_ids = post.tags.values_list('id', flat=True) #список id тегов flat=True - плоский список
    similar_posts = Post.published.filter(tags__in=post_tags_ids) \
        .exclude(id=post.id) # получение всех постов с такими тегами, исключая текущий пост
    similar_posts = similar_posts.annotate(same_tags=Count('tags')) \
                        .order_by('-same_tags', '-publish')[:4]
    # аггрегация Count для формирования поля same_tags + сортировка в убыв порядке по кол-ву совпад тегов
    return render(request, 'blog/post/detail.html', {'post' : post,
                                                     'comments' : comments,
                                                     'new_comment' : new_comment,
                                                     'comment_form' : comment_form,
                                                     'similar_posts': similar_posts})



def post_share(request, post_id):
    # поделиться постом
    post = get_object_or_404(Post, id=post_id, status='published')
    sent = False
    if request.method == "POST":
        # сохранение формы
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            # отправка почты
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = '{} ({}) прочти. Рекомендую! "{}"' \
                .format(cd['name'], cd['email'], post.title)
            message = 'Посмотри эту статью "{}" тут {}\n\n{}'.format(post.title, post_url, cd['name'])
            send_mail(subject, message, 'email', [cd['to']])
            sent = True
    else:
        form = EmailPostForm()

    return render(request, 'blog/post/share.html', {'post': post, 'sent': sent})

def post_search(request):
    form = SearchForm()
    query = None
    results = []
    if 'query' in request.GET:
        form = SearchForm(request.GET)
    if form.is_valid():
        query = form.cleaned_data['query']
        results = Post.objects.annotate(
            search=SearchVector('title', 'body')
        ).filter(search=query)
        # поиск на присутствуие query по полям title, body

    return render(request, 'blog/post/search.html', {'form': form,
                                                         'query': query,
                                                         'results': results})