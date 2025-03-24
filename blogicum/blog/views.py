from django.http import HttpResponseNotFound
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from .models import Post, Category


def post_filter():
    return Post.objects.filter(
        pub_date__lt=timezone.now(),
        is_published=True,
        category__is_published=True
    )


def index(request):
    latest_posts = post_filter().order_by('-pub_date')[:5]
    return render(
        request,
        'blog/index.html',
        {'post_list': latest_posts}
    )


def post_detail(request, id):  
    post = get_object_or_404(
        post_filter(),
        pk=id)
    return render(
        request,
        'blog/detail.html',
        {'post': post}
    )


def category_posts(request, category_slug):
    category = get_object_or_404(
        Category.objects.filter(is_published=True),
        slug=category_slug
    )
    posts_in_category = post_filter().filter(
        category=category
    ).order_by('-pub_date')
    
    return render(
        request,
        'blog/category.html',
        {
            'category': category,
            'post_list': posts_in_category
        }
    )