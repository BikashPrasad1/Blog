from django.shortcuts import render, get_object_or_404
from .models import Blog, Category

def posts_by_category(request, category_id):
    # Fetch posts belonging to this category
    posts = Blog.objects.filter(status='Published', category_id=category_id)
    category = get_object_or_404(Category, pk=category_id)

    context = {
        'posts': posts,
        'category': category,
    }
    return render(request, 'posts_by_category.html', context)

def blogs(request, slug):
    single_blog = get_object_or_404(Blog, slug=slug, status='Published')
    context = {
        'single_blog': single_blog,
    }
    return render(request, 'blog.html', context)

