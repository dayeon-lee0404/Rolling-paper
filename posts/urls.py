
from django.urls import path
from . import views

app_name = 'post'
urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('post_write/', views.post_write, name='post_write'),
    path('post_detail/<int:post_pk>/', views.post_detail, name='post_detail'),
    path('post_detail/<int:post_pk>/delete/', views.post_delete, name='post_delete'),
    path('post_detail/<int:post_pk>/modify/', views.post_modify, name='post_modify'),
    path('<int:pk>/comments/', views.comments_create, name='comments_create'),
    path('<int:post_pk>/comments/<int:comment_pk>/delete/', views.comments_delete, name='comments_delete'),
]