from django.urls import path
from . import views

app_name = 'post'
urlpatterns = [
    path('', views.index, name='index'),
    path('list/', views.post_list.as_view(), name='post_list'),
    path('mypage/', views.mypage, name='mypage'),
    path('post_write/', views.post_write, name='post_write'),
    path('post_detail/<int:id>/', views.post_detail, name='post_detail'),
    path('post_detail/<int:id>/delete/', views.post_delete, name='post_delete'),
    path('post_detail/<int:id>/modify/', views.post_modify, name='post_modify'),
    path('post/search/', views.post_search, name='post_search'),


    path('<int:id>/create_comments/', views.comments_input, name='comments_input'),
    path('<int:id>/comments/', views.comments_create, name='comments_create'),
    path('post_detail/comments/<int:comment_id>/delete/', views.comments_delete, name='comments_delete'),
    path('post_detail/<int:post_id>/comments/', views.comments_view, name='comments_view'),
    path('post_detail/<int:post_id>/comments/<int:comment_id>/', views.comments_detail, name='comments_detail'),
]
