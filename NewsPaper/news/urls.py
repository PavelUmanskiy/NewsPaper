from django.urls import path
from django.shortcuts import redirect

from .views import *


urlpatterns = [
    path('', PostList.as_view(), name='news'),
    path('create/', PostCreate.as_view(), name='post_create'),
    path('search/', PostSearch.as_view(), name='news_search'),
    path('<int:pk>/', PostDetail.as_view(), name='post_detail'),
    path('<int:pk>/edit/', PostUpdate.as_view(), name='post_edit'),
    path('<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),
    path('logout/', logout_user, name='logout'),
    path('upgrade/', upgrade_me, name='upgrade'),
    path('profile/<int:pk>/', UserDetail.as_view(), name='profile_detail'),
    path('profile/<int:pk>/edit/', UserUpdate.as_view(), name='profile_edit'),
    path('profile/<int:pk>/delete/', UserDelete.as_view(), name='profile_delete')
]
