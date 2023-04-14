from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from .models import Blog, Comment, Like, Tag
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required



def home(request):
    blogs = Blog.objects.all()
    paginator = Paginator(blogs, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'home.html', {'page_obj': page_obj})


def detail(request, blog_id):
    blog = get_object_or_404(Blog, pk=blog_id)
    comments = Comment.objects.filter(blog=blog)
    tags = blog.tag.all()
    like_count = len(Like.objects.filter(blog=blog))

    return render(request, 'detail.html', {'blog': blog, 'comments': comments, 'tags': tags, 'like_count':like_count})


def new(request):
    tags = Tag.objects.all()
    return render(request, 'new.html', {'tags': tags})


def create(request):
    new_blog = Blog()
    new_blog.title = request.POST.get('title')
    new_blog.content = request.POST.get('content')
    new_blog.image = request.FILES.get('image')
    new_blog.author = request.user

    new_blog.save()
    tags = request.POST.getlist('tags')

    for tag_id in tags:
        tag = Tag.objects.get(id=tag_id)
        new_blog.tag.add(tag)

    return redirect('detail', new_blog.id)


def edit(request, blog_id):
    # edit_blog = get_object_or_404(Blog, pk=blog_id)
    edit_blog = Blog.objects.get(id=blog_id)

    if request.user != edit_blog.author:
        return redirect('home')

    return render(request, 'edit.html', {'edit_blog': edit_blog})


def update(request, blog_id):
    old_blog = get_object_or_404(Blog, pk=blog_id)
    old_blog.title = request.POST.get('title')
    old_blog.content = request.POST.get('content')
    old_blog.image = request.FILES.get('image')
    old_blog.save()
    return redirect('detail', old_blog.id)


def delete(request, blog_id):
    delete_blog = get_object_or_404(Blog, pk=blog_id)
    delete_blog.delete()
    return redirect('home')


def create_comment(request, blog_id):
    comment = Comment()
    comment.content = request.POST.get('content')
    comment.blog = get_object_or_404(Blog, pk=blog_id)
    comment.author = request.user
    comment.save()
    return redirect('detail', blog_id)


def new_comment(request, blog_id):
    blog = get_object_or_404(Blog, pk=blog_id)
    return render(request, 'new_comment.html', {'blog': blog})



def like(request, blog_id):
    blog = get_object_or_404(Blog, pk=blog_id)
    #좋아요는 로그인 후 가능 -> 로그인 화면으로
    if request.user.is_anonymous:
        return redirect('login')
    
    # 동일 유저가 또 좋아요 누르면 좋아요 취소 
    else:
        like_check=Like.objects.filter(like_users=request.user, blog=blog)
        if like_check:
            like_check.delete()
            return redirect('detail', blog_id)
        # 좋아요 추가 
        else:
            like = Like()
            like.blog = get_object_or_404(Blog, pk=blog_id)
            like.like_users = request.user
            like.save()
            return redirect('detail', blog_id)
 
@login_required        
def commentlike(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.user == comment.author:
        messages.error(request,'본인이 작성한 댓글은 추천할 수 없습니다.')
        
    else:
        comment.like_user_comment.add(request.user)
    return redirect('detail', blog_id=comment.blog.id)


