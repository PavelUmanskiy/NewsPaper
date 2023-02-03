from django.shortcuts import render, redirect
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
    )
from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group

from .models import *
from .filters import *
from .forms import *
from .utils import UserIsAuthorOfPostMixin, UserIsOwnerOfProfileMixin
# Create your views here.


class PostList(ListView):
    model = Post
    ordering = '-time_create'
    template_name = 'main.html'
    context_object_name = 'posts'
    paginate_by = 3
    
    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context['is_not_author'] = not self.request.user.groups.filter(name='authors').exists()
        return context
    
        
class PostSearch(PostList):
    template_name = 'post_search.html'
    context_object_name = 'posts'
    paginate_by = 3

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


class PostCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_post',)
    template_name = 'post_create.html'
    form_class = PostForm


class PostUpdate(PermissionRequiredMixin, UserIsAuthorOfPostMixin, UpdateView):
    permission_required = ('news.change_post',)
    template_name = 'post_update.html'
    form_class = PostForm
    
    def get_object(self, **kwargs) -> models.Model:
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)


class PostDelete(PermissionRequiredMixin, UserIsAuthorOfPostMixin, DeleteView):
    permission_required = ('news.delete_post',)
    template_name = 'post_delete.html'
    queryset = Post.objects.all()
    success_url = '/news/'


class UserDetail(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'user.html'
    context_object_name = 'user'


class UserUpdate(LoginRequiredMixin, UserIsOwnerOfProfileMixin, UpdateView):
    template_name = 'user_update.html'
    form_class = UserForm
    
    def dispatch(self, request, *args, **kwargs):
        print(self.request, kwargs)
        return super().dispatch(request, *args, **kwargs)
    
    def get_object(self, **kwargs) -> models.Model:
        id = self.kwargs.get('pk')
        return User.objects.get(pk=id)


class UserDelete(LoginRequiredMixin, UserIsOwnerOfProfileMixin, DeleteView):
    template_name = 'user_delete.html'
    queryset = User.objects.all()
    success_url = '/news/'


@login_required
def upgrade_me(request):
    user = request.user
    premium_group = Group.objects.get(name='authors')
    
    if not request.user.groups.filter(name='authors').exists():
        premium_group.user_set.add(user)
    
    Author.objects.create(user_id=request.user.pk)
    return redirect('news')


def logout_user(request):
    logout(request)
    return redirect('news')