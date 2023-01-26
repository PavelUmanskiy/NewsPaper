from django.shortcuts import render
from django.views.generic import ListView, DetailView

from .models import *
from .filters import *
# Create your views here.


class PostList(ListView):
    model = Post
    ordering = '-time_create'
    template_name = 'main.html'
    context_object_name = 'posts'
    paginate_by = 10
    
    
class PostSearch(PostList):
    template_name = 'post_search.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset())
        return context


class PostDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'
    

