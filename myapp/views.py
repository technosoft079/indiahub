from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404

from django.contrib.auth.forms import AuthenticationForm

from django.contrib.auth import login, logout

from django.contrib.auth.decorators import login_required

from .forms import RegisterForm, NewsForm, CommentForm

from .models import News, Comment, Category

from django.core.paginator import Paginator
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import NewsSerializer


def test(request):
    return HttpResponse("OK")

def home(request):

    query = request.GET.get('q')

    categories = Category.objects.all()

    if query:

        news = News.objects.filter(title__icontains=query)

    else:

        news_list = News.objects.all().order_by('-created_at')

        paginator = Paginator(news_list, 6)

        page_number = request.GET.get('page')

        news = paginator.get_page(page_number)

    return render(request, 'home.html', {
        'news': news,
        'categories': categories
    })


def register_view(request):

    if request.method == 'POST':

        form = RegisterForm(request.POST)

        if form.is_valid():

            user = form.save()

            login(request, user)

            return redirect('home')

    else:
        form = RegisterForm()

    return render(request, 'register.html', {'form': form})


def login_view(request):

    if request.method == 'POST':

        form = AuthenticationForm(data=request.POST)

        if form.is_valid():

            user = form.get_user()

            login(request, user)

            return redirect('home')

    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form})


def logout_view(request):

    logout(request)

    return redirect('home')


@login_required
def dashboard(request):

    news = News.objects.filter(author=request.user)

    return render(request, 'dashboard.html', {'news': news})


@login_required
def create_news(request):

    if request.method == 'POST':

        form = NewsForm(request.POST, request.FILES)

        if form.is_valid():

            news = form.save(commit=False)

            news.author = request.user

            news.save()

            return redirect('home')

    else:

        form = NewsForm()

    return render(request, 'create_news.html', {'form': form})


def news_detail(request, id):

    news = get_object_or_404(News, id=id)

    comments = Comment.objects.filter(news=news).order_by('-created_at')

    if request.method == 'POST':

        if request.user.is_authenticated:

            form = CommentForm(request.POST)

            if form.is_valid():

                comment = form.save(commit=False)

                comment.user = request.user

                comment.news = news

                comment.save()

                return redirect('news_detail', id=id)

    else:

        form = CommentForm()

    return render(request, 'news_detail.html', {
        'news': news,
        'comments': comments,
        'form': form
    })

@login_required
def update_news(request, id):

    news = get_object_or_404(News, id=id)

    if request.user != news.author:
        return redirect('home')

    if request.method == 'POST':

        form = NewsForm(request.POST, request.FILES, instance=news)

        if form.is_valid():

            form.save()

            return redirect('dashboard')

    else:

        form = NewsForm(instance=news)

    return render(request, 'update_news.html', {'form': form})


@login_required
def delete_news(request, id):

    news = get_object_or_404(News, id=id)

    if request.user == news.author:

        news.delete()

    return redirect('dashboard')

@login_required
def like_news(request, id):

    news = get_object_or_404(News, id=id)

    if request.user in news.likes.all():

        news.likes.remove(request.user)

    else:

        news.likes.add(request.user)

    return redirect('news_detail', id=id)

@api_view(['GET'])
def api_news(request):

    news = News.objects.all()

    serializer = NewsSerializer(news, many=True)

    return Response(serializer.data)


def category_news(request, id):

    category = get_object_or_404(Category, id=id)

    news = News.objects.filter(category=category)

    categories = Category.objects.all()

    return render(request, 'category.html', {
        'news': news,
        'categories': categories,
        'selected_category': category
    })  