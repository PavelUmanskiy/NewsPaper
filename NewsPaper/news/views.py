from django.shortcuts import render
from django.views.generic import ListView, DetailView

from .models import *
# Create your views here.


class PostList(ListView):
    model = Post
    ordering = '-time_create'
    template_name = 'main.html'
    context_object_name = 'posts'


class PostDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'