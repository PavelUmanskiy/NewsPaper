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
from django.core.mail import send_mail

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
    def dispatch(self, request, *args, **kwargs):
        print('########################################################')
        print(self.request, self.request.user)
        print('########################################################')
        return super().dispatch(request, *args, **kwargs)

class PostCreate(PermissionRequiredMixin, CreateView): 
    permission_required = ('news.add_post',)
    template_name = 'post_create.html'
    form_class = PostForm
    
    # def post(self, request, *args, **kwargs):
    #     form = self.form_class(request.POST, data={'author_id': Author.objects.get(user__id=self.request.user.id).pk})  
    #     if form.is_valid(): # если пользователь ввёл всё правильно и нигде не ошибся, то сохраняем новый товар
    #         form.save()
    #     return super().get(request, *args, **kwargs)
    
    # def dispatch(self, request, *args, **kwargs):
    #     print('########################################################')
    #     print(self.request)
    #     print('########################################################')
    #     return super().dispatch(request, *args, **kwargs)
    
    #def post(self, request, *args, **kwargs):
    #    send_mail(
    #            subject=f'Новый пост в категории',  # подгрузить категорию
    #            message=appointment.message,  # сообщение с кратким описанием проблемы
    #            from_email='', # мой email для спама
    #            recipient_list=[]  # здесь список получателей (те, кто подписались)
    #    )
    #    return super().post(request, *args, **kwargs)


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