from django.shortcuts import get_object_or_404, render
from django.utils import timezone

from .models import Category, Post

POSTS_ON_MAIN = 5


def filter_published_posts(posts):
    """Оставить только посты, которые можно показывать на сайте."""
    return posts.select_related(
        'author', 'category', 'location'
    ).filter(
        is_published=True,
        pub_date__lte=timezone.now(),
        category__is_published=True,
    )


def index(request):
    post_list = filter_published_posts(Post.objects)[:POSTS_ON_MAIN]
    return render(request, 'blog/index.html', {'post_list': post_list})


def post_detail(request, post_id):
    post = get_object_or_404(filter_published_posts(Post.objects), pk=post_id)
    return render(request, 'blog/detail.html', {'post': post})


def category_posts(request, category_slug):
    category = get_object_or_404(
        Category, slug=category_slug, is_published=True
    )
    post_list = filter_published_posts(category.posts)
    return render(
        request,
        'blog/category.html',
        {'category': category, 'post_list': post_list},
    )
