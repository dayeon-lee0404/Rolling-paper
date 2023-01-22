from django.db import models
from django.conf import settings
from common.models import User

class Post(models.Model):
    title = models.CharField(max_length=64, verbose_name='글 제목')
    contents = models.TextField(verbose_name='글 내용')
    writer = models.ForeignKey('common.User', on_delete=models.CASCADE, verbose_name='작성자')
    write_dttm = models.DateTimeField(auto_now_add=True, verbose_name='글 작성일')

    post_name = models.CharField(max_length=32, default='Python', verbose_name='게시판 종류')
    update_dttm = models.DateTimeField(auto_now=True, verbose_name='마지막 수정일')

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'post'
        verbose_name = '게시판'
        verbose_name_plural = '게시판'


class Comment(models.Model):
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment_writer = models.ForeignKey('common.User', on_delete=models.CASCADE, verbose_name='댓글 작성자')
    content = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.content

