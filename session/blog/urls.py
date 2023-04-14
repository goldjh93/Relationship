from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'), # 127.0.0.1:8000
    path('blog/<int:blog_id>/', views.detail, name='detail'),
    path('blog/new/', views.new, name='new'),
    path('blog/create/', views.create, name='create'),
    path('blog/edit/<int:blog_id>/', views.edit, name='edit'),
    path('blog/update/<int:blog_id>/', views.update, name='update'),
    path('blog/delete/<int:blog_id>/', views.delete, name='delete'),
    path('blog/new_comment/<int:blog_id>/', views.new_comment, name='new_comment'),
    path('blog/create_comment/<int:blog_id>/', views.create_comment, name='create_comment'),
    path('blog/likes/<int:blog_id>/', views.like, name='likes'),
    path('blog/comments/<int:comment_id>/likes', views.commentlike, name='commentlikes'),
]