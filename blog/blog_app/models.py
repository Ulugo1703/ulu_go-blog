from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Category(models.Model):
    title = models.CharField(max_length=255, verbose_name='Название категории')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['-title']


class Article(models.Model):
    title = models.CharField(max_length=255, verbose_name='Название статьи', unique=True)
    short_description = models.TextField(verbose_name='Краткое описание', max_length=100)
    full_description = models.TextField(verbose_name='Полное описание')
    image = models.ImageField(verbose_name='Фото', upload_to='articles/photos/', blank=True, null=True)
    views = models.PositiveIntegerField(verbose_name='Кол-во просмотров', default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория', related_name='articles')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор', related_name='articles')

    def get_absolute_url(self):
        return reverse('detail', kwargs={'pk': self.pk})

    def get_image(self):
        if self.image:
            return self.image.url
        return 'https://sun9-60.userapi.com/impf/996Uzho6TCPhP6BYLquQVF9azuhm_ko7TkTEoA/4DKBnJPhuFc.jpg?size=498x281&quality=96&sign=91adc9495d16f77972ff7c11748f8b8e&type=album'

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'
        ordering = ['-created_at']


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='comments')
    created_at = models.DateTimeField(auto_now_add=True)
    text = models.TextField()


class CommentReply(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='replied_comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='replied_comments')
    created_at = models.DateTimeField(auto_now_add=True)
    text = models.TextField()


class ArticleCountView(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    session_id = models.CharField(max_length=255)


class Like(models.Model):
    user = models.ManyToManyField(User, related_name='likes')
    article = models.OneToOneField(Article, on_delete=models.CASCADE, related_name='likes')
    comment = models.OneToOneField(Comment, on_delete=models.CASCADE, related_name='likes', null=True)


class Dislike(models.Model):
    user = models.ManyToManyField(User, related_name='dislikes')
    article = models.OneToOneField(Article, on_delete=models.CASCADE, related_name='dislikes')
    comment = models.OneToOneField(Comment, on_delete=models.CASCADE, related_name='dislikes', null=True)

