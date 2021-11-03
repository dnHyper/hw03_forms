from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render
from django.http import JsonResponse
from django.db.models import Count

from yatube.settings import (EMAIL_ADMIN, NUMBER_OF_PAGES,
                             NUMBER_OF_GROUP_PAGES)

from .forms import FeedBackForm, PostForm
from .models import Group, Post, User, VotePost


def page_not_found_view(request, exception):
    """Метод для вывода отдельной страницы c ошибкой."""
    return render(request, '404.html', status=404)


def index(request):
    """Вывод главной страницы + лайки"""
    posts = Post.objects.select_related('group', 'author').annotate(
        count=Count('posts'))
    paginator = Paginator(posts, NUMBER_OF_PAGES)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'page_obj': page_obj, }
    return render(request, 'posts/index.html', context)


def group_posts(request, slug):
    """Вывод списка записей от группы."""
    group = get_object_or_404(Group, slug=slug)
    posts = group.posts.select_related('author').annotate(
        count=Count('posts'))
    paginator = Paginator(posts, NUMBER_OF_PAGES)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'page_obj': page_obj,
               'group': group, }
    return render(request, 'posts/group_list.html', context)


def groups(request):
    """Вывода списка групп."""
    groups = Group.objects.all()
    paginator = Paginator(groups, NUMBER_OF_GROUP_PAGES)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'page_obj': page_obj}
    return render(request, 'posts/groups.html', context)


def profile(request, username):
    """Вывод страницы пользователя со списком сообщений"""
    user = get_object_or_404(User, username=username)
    posts = user.posts.select_related('author', 'group').annotate(
        count=Count('posts'))
    paginator = Paginator(posts, NUMBER_OF_PAGES)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'username': user,
               'page_obj': page_obj, }
    return render(request, 'posts/profile.html', context)


def post_detail(request, post_id):
    """Вывод информации о сообщении"""
    post = get_object_or_404(Post.objects.select_related('group', 'author').annotate(
        count=Count('posts')), pk=post_id)
    context = {'post': post, }
    return render(request, 'posts/post_detail.html', context)


@login_required
def post_create(request):
    """Создание нового сообщения: только для авторизированного пользователя"""
    form = PostForm(request.POST or None, files=request.FILES or None)
    if form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.save()
        return redirect('posts:profile', request.user)
    return render(request, 'posts/post_create.html', {'form': form})


@login_required
def post_edit(request, post_id):
    """Редактирование сообщения: только для авторизированного пользователя и
    только для создателя данного сообщения."""
    post = get_object_or_404(Post, pk=post_id)
    if post.author.pk != request.user.id:
        return redirect('posts:post_detail', post_id)

    form = PostForm(request.POST or None, instance=post)
    if form.is_valid():
        form.save()
        return redirect('posts:post_detail', post_id)
    context = {'post_id': post_id,
               'form': form, }
    return render(request, 'posts/post_create.html', context)


def send_msg(email, name, text):
    """Метод отправки письма"""
    subject = "Вам оставили сообщение"
    body = f"""На вашем сайте, через форму обратной связи, было оставлено
    сообщение.

    {name} пишет:
    {text}

    """
    send_mail(
        subject, body, email, EMAIL_ADMIN,
    )


def feedback(request):
    """Куда на сайте без формы обратной связи то?"""
    form = FeedBackForm(request.POST)
    if form.is_valid():
        send_msg(form.cleaned_data['email'],
                 form.cleaned_data['name'],
                 form.cleaned_data['text'],)
        return redirect('posts:feedback_done')
    context = {'form': form, }
    return render(request, 'posts/feedback.html', context)


def feedback_done(request):
    return render(request, 'posts/feedback_done.html')


@login_required
def votepost(request):
    """Какая соц.сеть без лайков?"""
    if request.is_ajax():
        post = request.POST.get('post', None)
        vote = VotePost.objects.filter(
            user__id=request.user.id).filter(post=post)
        post = get_object_or_404(Post, pk=post)
        if not vote.exists():
            VotePost.objects.create(user=request.user, post=post)
            return JsonResponse({"status": 'add'}, status=200)
        else:
            vote.delete()
            return JsonResponse({"status": 'del'}, status=200)
    return render(request, "posts/votepost.html")
