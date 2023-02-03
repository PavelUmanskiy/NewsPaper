from django.db import models
from django.db.models import Sum
from django.contrib.auth.models import User
from django.urls import reverse

from .utils import *


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT, verbose_name='Имя')
    rating = models.IntegerField(default=0)
    
    def update_rating(self):
        rating_of_posts_by_author = Post.objects.filter(author=self).aggregate(Sum('rating'))['rating__sum'] * 3
        rating_of_comments_by_author = Comment.objects.filter(user=self.user).aggregate(Sum('rating'))['rating__sum']
        rating_of_comments_under_posts_of_author = Comment.objects.filter(post__author__user=self.user).aggregate(Sum('rating'))['rating__sum']
        
        self.rating = rating_of_posts_by_author + rating_of_comments_by_author + rating_of_comments_under_posts_of_author
        self.save()


class Category(models.Model):
    name = models.CharField(max_length=72, unique=True, verbose_name='Категории')
    
    def __str__(self) -> str:
        return self.name

class PostCategory(models.Model):
    post = models.ForeignKey('Post', on_delete=models.PROTECT)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)

class Post(LikeMixin, models.Model):
    news = 'NE'
    article = 'AR'
    
    POST_TYPES = [
        (news, 'Новость'),
        (article, 'Статья'),
    ]
    
    author = models.ForeignKey(Author, on_delete=models.PROTECT, verbose_name='Автор')
    post_type = models.CharField(max_length=2, choices=POST_TYPES, default=article, verbose_name='Вид поста')
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    time_update = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')
    categories = models.ManyToManyField(Category, through=PostCategory)
    title = models.CharField(max_length=72, default='Defaullt title', verbose_name='Заголовок')
    content = models.CharField(max_length=2048, default='Default content', verbose_name='Контент')
    rating = models.IntegerField(default=0)
    
    def preview(self):
        return self.content[:124] + '...' if len(self.content) > 124 else self.content
    
    def get_absolute_url(self):
        return reverse("post", kwargs={"pk": self.pk})
    
    
class Comment(LikeMixin, models.Model):
    post = models.ForeignKey(Post, on_delete=models.PROTECT, verbose_name='Пост')
    user = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name='Пользователь')
    content = models.CharField(max_length=512, default='Default comment', verbose_name='Комментарий')
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Время создания комментария')
    rating = models.IntegerField(default=0)