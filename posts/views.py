from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from posts.forms import CommentForm
from posts.models import Post, Comment
import re
from django.views.generic.list import ListView
from django.shortcuts import render, redirect
from .forms import PostWriteForm
from .models import Post
from common.models import User
from common.decorators import login_message_required
from django.shortcuts import get_object_or_404
from datetime import date, datetime, timedelta


# Create your views here.


def index(request):
    return render(request, 'posts/index.html')


@require_POST
def comments_create(request, id):
    if request.user.is_authenticated:
        post = get_object_or_404(Post, id=id)
        user = request.user
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post_id = post
            comment.comment_writer = user
            comment.save()
        return redirect(f'/post_detail/{id}/')
    return redirect('login')


@require_POST
def comments_delete(request, comment_id):
    if request.user.is_authenticated:
        comment = get_object_or_404(Comment, id=comment_id)
        post_id = comment.post_id.id
        if request.user == comment.comment_writer:
            comment.delete()
    return redirect(f'/post_detail/{post_id}/')


@require_POST
def comments_view(request, post_id):
    if request.method == 'GET':
        return redirect(f'/post_detail/{post_id}/')
    if request.user.is_authenticated:
        comments = Comment.objects.filter(post_id=post_id)
        context = {'comments': comments}
        response = render(request, 'posts/comments.html', context)
        return response


class post_list(ListView):
    model = Post
    ordering = '-write_dttm'
    paginate_by = 10


def post_detail(request, id):
    post = get_object_or_404(Post, id=id)
    comments = Comment.objects.filter(post_id=id)
    #dday가 되었는지 판단
    dday = str(post.dday_ddmt)[:10]
    write_ddmt = str(post.write_dttm)[:10]
    is_dday = dday <= write_ddmt
    print(is_dday, dday, write_ddmt)
    context = {'post': post, 'comments': comments, 'is_dday': is_dday, 'dday' : dday}
    response = render(request, 'posts/post_detail.html', context)
    return response


def comments_input(request, id):
    post = get_object_or_404(Post, id=id)
    context = {'post': post}
    response = render(request, 'posts/create_comment.html', context)
    return response

@login_message_required
def post_write(request):
    if request.method == 'GET':
        write_form = PostWriteForm()
        context = {'forms': write_form}
        return render(request, 'posts/post_write.html', context)

    elif request.method == 'POST':
        write_form = PostWriteForm(request.POST)
        dday_ddmt = request.POST['dday_ddmt']
        if write_form.is_valid() and dday_ddmt != '':
            writer = request.user
            post = Post(
                title=write_form.title,
                contents=write_form.contents,
                writer=writer,
                post_name=write_form.post_name,
                dday_ddmt=dday_ddmt,
            )
            post.save()
            return redirect('/list')
        else:
            context = {'forms': write_form}
            if write_form.errors:
                for value in write_form.errors.values():
                    context['error'] = value
            if dday_ddmt == '':
                context['error'] = '날짜를 선택하세요'
                return render(request, 'posts/post_write.html', context)
            return render(request, 'posts/post_list.html', context)


@login_message_required
def post_modify(request, id):
    login_session = request.session.get('request.user', '')
    context = {'login_session': login_session}

    post = get_object_or_404(Post, id=id)
    context['post'] = post

    if post.writer != request.user:
        return redirect(f'/post_detail/{id}/')

    if request.method == 'GET':
        write_form = PostWriteForm(instance=post)
        context['forms'] = write_form
        return render(request, 'posts/post_modify.html', context)

    elif request.method == 'POST':
        write_form = PostWriteForm(request.POST)

        if write_form.is_valid():
            post.title = write_form.title
            post.contents = write_form.contents
            post.post_name = write_form.post_name
            post.save()
            return redirect(f'/post_detail/{id}/')
        else:
            context['forms'] = write_form
            if write_form.errors:
                for value in write_form.errors.values():
                    context['error'] = value
            return render(request, 'posts/post_modify.html', context)


@login_message_required
def mypage(request):
    if request.user.is_authenticated:
        user = request.user
        posts = Post.objects.filter(writer=user)
        context = {'posts': posts}
        return render(request, 'posts/mypage.html', context)
    return redirect('/login')


def post_delete(request, id):
    post = get_object_or_404(Post, id=id)
    if post.writer == request.user:
        post.delete()
        return redirect('/list')
    else:
        return redirect(f'/post_detail/{id}/')
