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
from .utils import (
    UserIsAuthorOfPostMixin, 
    UserIsOwnerOfProfileMixin, 
    my_HTTP_request_console_log, 
)


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
        request.session['post_id_for_subscription'] = request.path.partition('news')[2][1:-1]  # post_id нужен только для подписки
        # my_HTTP_request_console_log(request=request)
        return super().dispatch(request, *args, **kwargs)

class PostCreate(PermissionRequiredMixin, CreateView): 
    permission_required = ('news.add_post',)
    template_name = 'post_create.html'
    form_class = PostForm
    
    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author = Author.objects.get(user_id=self.request.user.id)
        return super().form_valid(form)
    
    def dispatch(self, request, *args, **kwargs):
        # my_HTTP_request_console_log(request=request)
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        # my_HTTP_request_console_log(request=request)
        # author, categories_names, recipient_list = email_info(self=self, request=request)
        # if recipient_list:
        #     send_mail(
        #             subject="Новый пост в категории " +
        #             f" {categories_names}" +
        #             f"от {author}",
        #             message=request.POST['content'][:50],  # сообщение с превью статьи
        #             from_email=DEFAULT_FROM_EMAIL,
        #             recipient_list=recipient_list # здесь список получателей (те, кто подписались)
        #     )
        return super().post(request, *args, **kwargs)


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

@login_required
def subscribe(request):
    post_id = request.session.get('post_id_for_subscription')
    
    post_categories = Post.objects.get(id=post_id).categories.values_list('id')
    post_author = Post.objects.get(pk=post_id).author_id
    
    if not Subscriber.objects.filter(user=request.user).exists():
        subscriber = Subscriber.objects.create(user=request.user)
        print(f'new subscriber {subscriber} created')
    else:
        subscriber = Subscriber.objects.get(user=request.user)
        print(f'subscriber {subscriber} already exists')
    
    categories_subscribed = [dict_['id']  for dict_ in subscriber.categories.values('id')]
    for post_category in post_categories:
        if post_category[0] not in categories_subscribed:
            subscriber.categories.add(post_category[0])
            print(f'subscribtion on category {post_category[0]} executed')
            
    authors_subscribed = [dict_['id']  for dict_ in subscriber.authors.values('id')]
    if post_author not in authors_subscribed:
        subscriber.authors.add(post_author)
        print(f'subscription on author {post_author} executed')
    return redirect(f'{post_id}/')