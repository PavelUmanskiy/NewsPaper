from django.urls import path

from .views import *


urlpatterns = [
    path('news/', PostList.as_view(), name='news'),
    path('news/create/', PostCreate.as_view(), name='post_create'),
    path('news/search/', PostSearch.as_view(), name='news_search'),
    path('news/<int:pk>/', PostDetail.as_view(), name='post_detail'),
    path('news/<int:pk>/edit/', PostUpdate.as_view(), name='post_edit'),
    path('news/<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),
]
