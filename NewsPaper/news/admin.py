from django.contrib import admin
from .models import *
# Register your models here.

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author', 'time_create', 'rating')
    list_display_links = ('id', 'title')
    search_fields = ('title', 'content', 'author__user_username', 'categories')
    list_editable = ('rating',)
    list_filter = ('categories', 'time_create', 'rating')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('name',)


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'rating')
    list_display_links = ('id', 'user')
    search_fields = ('user',)
    list_editable = ('rating',)
    list_filter = ('rating',)


@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    list_display = ('id', 'user')
    list_display_links = ('id', 'user')
    search_fields = ('user',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'content', 'time_create', 'rating')
    list_display_links = ('id', 'content')
    search_fields = ('post__title', 'user', 'content')
    list_filter = ('user', 'time_create', 'rating')
    list_editable = ('rating',)


