from django.shortcuts import render
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
    )
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import *
from .filters import *
from .forms import *
# Create your views here.


class PostList(ListView):
    model = Post
    ordering = '-time_create'
    template_name = 'main.html'
    context_object_name = 'posts'
    paginate_by = 3
    
        
class PostSearch(PostList):
    template_name = 'post_search.html'
    context_object_name = 'filter'
    
    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = self.filterset
        return context


class PostDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'


class PostCreate(CreateView):
    template_name = 'post_create.html'
    form_class = PostForm


class PostUpdate(UpdateView):
    template_name = 'post_update.html'
    form_class = PostForm
    
    def get_object(self, **kwargs) -> models.Model:
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)


class PostDelete(DeleteView):
    template_name = 'post_delete.html'
    queryset = Post.objects.all()
    success_url = '/news/'
