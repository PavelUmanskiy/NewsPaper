from django_filters import FilterSet, NumberFilter, CharFilter, \
ModelMultipleChoiceFilter, ChoiceFilter, LookupChoiceFilter, DateFilter

from .models import *


class PostFilter(FilterSet):
    author__user__username = CharFilter(field_name='author__user__username', lookup_expr='icontains', 
                                        label='Фильтр по автору')
    
    title = CharFilter(field_name='title', lookup_expr='icontains', label='Фильтр по названию')
    
    post_type = ChoiceFilter(choices=Post.POST_TYPES)
    
    categories = ModelMultipleChoiceFilter(field_name='categories', label='Фильтр по категориям',
                                           queryset=Category.objects.all())
    
    rating = NumberFilter(field_name='rating', label='Фильтр по рейтингу')
    
    time_create = DateFilter(field_name='time_create', lookup_expr='gte', label='Фильтр по дате')
    
    class Meta():
        model = Post
        fields = [
            'author__user__username',
            'title',
            'post_type',
            'categories',
            'rating',
            'time_create'
            ]
