from django.shortcuts import render, HttpResponse, redirect
from .models import Category, Article, Comment, ArticleCountView, Like, Dislike
from .forms import LoginForm, RegistrationForm, ArticleForm, CommentForm, CommentReplyForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import UpdateView, DeleteView
# Create your views here.


def home_view(request):
    articles = Article.objects.all()

    context = {
        'articles': articles
    }
    return render(request, 'blog_app/index.html', context)


def search(request):
    search_query = request.GET.get('q')
    articles = Article.objects.filter(
        title__iregex=search_query
    )
    context = {
        'articles': articles
    }
    return render(request, 'blog_app/index.html', context)


def category_articles(request, pk):
    category = Category.objects.get(pk=pk)  # отдает 1 элемент
    articles = Article.objects.filter(category=category)
    context = {
        'category': category,
        'articles': articles
    }
    return render(request, 'blog_app/index.html', context)


def article_detail(request, pk):
    article = Article.objects.get(pk=pk)
    author = request.user
    # 1
    # comments = Comment.objects.filter(article=article)
    # 2
    comments = article.comments.all()
    try:
        article.likes
    except Exception as e:
        Like.objects.create(article=article)
    try:
        article.dislikes
    except Exception as e:
        Dislike.objects.create(article=article)

    if request.method == 'POST':
        if 'reply_to' in request.GET:
            comment = Comment.objects.get(pk=request.POST['_comment_id'])
            form = CommentReplyForm(data=request.POST)
            if form.is_valid():
                form = form.save(commit=False)
                form.comment = comment
                form.author = author
                form.save()
                messages.success(request, 'Ответили на комментарий')
                return redirect('detail', article.pk)
        else:
            form = CommentForm(data=request.POST)
            if form.is_valid():
                form = form.save(commit=False)
                form.article = article
                form.author = author
                form.save()
                messages.success(request, 'Комментарий успешно оставлен')
                return redirect('detail', article.pk)
    else:
        if 'reply_to' in request.GET:
            form = CommentReplyForm()
        else:
            form = CommentForm()

    if not request.session.session_key:
        request.session.save()

    session_id = request.session.session_key

    viewed_articles = ArticleCountView.objects.filter(article=article, session_id=session_id)

    if viewed_articles.count() == 0 and session_id != 'None':
        viewed = ArticleCountView()
        viewed.article = article
        viewed.session_id = session_id
        viewed.save()

        article.views += 1
        article.save()

    likes = article.likes.user.all().count()
    dislikes = article.dislikes.user.all().count()
    print(likes, dislikes)

    context = {
        'article': article,
        'form': form,
        # 'reply_form':
        'comments': comments,
        'likes': likes,
        'dislikes': dislikes
    }
    return render(request, 'blog_app/detail.html', context)


def log_in(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')

    else:
        form = LoginForm()
    context = {
        'form': form
    }
    return render(request, 'blog_app/login.html', context)


def sign_up(request):
    if request.method == 'POST':
        form = RegistrationForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegistrationForm()

    context = {
        'form': form
    }
    return render(request, 'blog_app/registration.html', context)


def user_logout(request):
    logout(request)
    return redirect('home')


def create_article(request):
    user = request.user

    if request.method == 'POST':
        form = ArticleForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            form = form.save(commit=False)
            form.author = user
            form.save()
            messages.success(request, 'Статья успешно добавлена')
            return redirect('detail', form.pk)
        else:
            messages.error(request, 'Что-то пошло не так')
            return redirect('detail', form.pk)

    else:
        form = ArticleForm()

    context = {
        'form': form
    }
    return render(request, 'blog_app/article_form.html', context)


class ArticleUpdateView(UpdateView):
    model = Article
    form_class = ArticleForm
    template_name = 'blog_app/article_form.html'


class ArticleDeleteView(DeleteView):
    model = Article
    template_name = 'blog_app/article_confirm_delete.html'
    success_url = '/'


def delete_comment(request, comment_id):
    comment = Comment.objects.get(pk=comment_id)

    if request.user.is_superuser or request.user == comment.author:
        messages.success(request, 'Комментарий удален')
        comment.delete()
        return redirect('detail', comment.article.pk)
    messages.error(request, 'У вас нет прав на удаление')
    return redirect('detail', comment.article.pk)


def add_vote(request, obj_type, obj_id, action):
    from django.shortcuts import get_object_or_404

    obj = None

    if obj_type == 'article':
        obj = get_object_or_404(Article, pk=obj_id)
    elif obj_type == 'comment':
        obj = get_object_or_404(Comment , pk=obj_id)

    try:
        obj.likes
    except Exception as e:
        if obj.__class__ is Article:
            Like.objects.create(article=obj)
        else:
            Like.objects.create(comment=obj)

    try:
        obj.dislikes
    except Exception as e:
        if obj.__class__ is Article:
            Dislike.objects.create(article=obj)
        else:
            Dislike.objects.create(comment=obj)

    if action == 'add_like':
        if request.user in obj.likes.user.all():
            obj.likes.user.remove(request.user.pk)  # удаляем объект пользователя добавившего лайк
        else:
            obj.likes.user.add(request.user.pk)
            obj.dislikes.user.remove(request.user.pk)

    elif action == 'add_dislike':
        if request.user in obj.dislikes.user.all():
            obj.dislikes.user.remove(request.user.pk)  # удаляем объект пользователя добавившего лайк
        else:
            obj.dislikes.user.add(request.user.pk)
            obj.likes.user.remove(request.user.pk)

    return redirect(request.environ['HTTP_REFERER'])


@login_required(login_url='/login/', redirect_field_name='user_articles')
def user_articles(request):
    from django.utils.timezone import now
    articles = Article.objects.filter(author=request.user)
    likes = [article.likes.user.all().count() for article in articles]
    views = [article.views for article in articles]

    context = {
        'articles': articles,
        'likes': sum(likes),
        'views': sum(views),
        'days': (now() - request.user.date_joined).days

    }
    return render(request, 'blog_app/user_articles.html', context)
