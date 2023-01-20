from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from posts.forms import CommentForm
from posts.models import Post, Comment

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
def comments_create(request, pk):
    if request.user.is_authenticated:
        post = get_object_or_404(Post, pk=pk)
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.comment_writer = request.user
            comment.save()
        return redirect('post:detail', post.pk)
    return redirect('login')


@require_POST
def comments_delete(request, post_pk, comment_pk):
    if request.user.is_authenticated:
        comment = get_object_or_404(Comment, pk=comment_pk)
        if request.user == comment.user:
            comment.delete()
    return redirect('post:detail', post_pk)


def post_list(request):
    login_session = request.session.get('login_session', '')
    context = {'login_session': login_session}
    return render(request, 'posts/post_list.html', context)


def post_detail(request, pk):
    login_session = request.session.get('login_session', '')
    context = {'login_session': login_session}
    post = get_object_or_404(Post, id=pk)
    context['post'] = post

    # 글쓴이인지 확인
    if post.writer.username == login_session:
        context['writer'] = True
    else:
        context['writer'] = False

    response = render(request, 'posts/post_detail.html', context)

    # 조회수 기능(쿠키이용)
    expire_date, now = datetime.now(), datetime.now()
    expire_date += timedelta(days=1)
    expire_date = expire_date.replace(hour=0, minute=0, second=0, microsecond=0)
    expire_date -= now
    max_age = expire_date.total_seconds()
    return response


@login_message_required
def post_write(request):
    login_session = request.session.get('login_session', '')
    context = {'login_session': login_session}

    if request.method == 'GET':
        write_form = PostWriteForm()
        context['forms'] = write_form
        return render(request, 'posts/post_write.html', context)

    elif request.method == 'POST':
        write_form = PostWriteForm(request.POST)

        if write_form.is_valid():
            print(User.objects.get(email=login_session))
            writer = User.objects.get(email=login_session)
            post = Post(
                title=write_form.title,
                contents=write_form.contents,
                writer = writer,
                post_name=write_form.post_name
            )
            post.save()
            return redirect('/posts/index.html')
        else:
            context['forms'] = write_form
            if write_form.errors:
                for value in write_form.errors.values():
                    context['error'] = value
            return render(request, 'posts/post_write.html', context)


@login_message_required
def post_modify(request, pk):
    login_session = request.session.get('login_session', '')
    context = {'login_session': login_session}

    post = get_object_or_404(Post, id=pk)
    context['post'] = post

    if post.writer.username != login_session:
        return redirect(f'/posts/detail/{pk}/')

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
            return redirect('/posts')
        else:
            context['forms'] = write_form
            if write_form.errors:
                for value in write_form.errors.values():
                    context['error'] = value
            return render(request, 'posts/post_modify.html', context)


def post_delete(request, pk):
    login_session = request.session.get('login_session', '')
    post = get_object_or_404(Post, id=pk)
    if post.writer.username == login_session:
        post.delete()
        return redirect('/posts')
    else:
        return redirect(f'/posts/detail/{pk}/')
