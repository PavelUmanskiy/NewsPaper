from django_filters import FilterSet, NumberFilter, CharFilter, \
MultipleChoiceFilter, ChoiceFilter, LookupChoiceFilter, DateFilter

from .models import *


class DataProvider():
    @classmethod
    def get_categories_names_for_choices(cls) -> list:
        categories_queryset = Post.objects.values_list('categories__name').distinct()
        categories_names = [_ for _ in categories_queryset]
        result = []
        for category, name in categories_queryset, categories_names:
            result.append((category, name))
        return result


class PostFilter(FilterSet):
    author__user__username = CharFilter(field_name='author__user__username', lookup_expr='icontains', 
                                        label='Фильтр по автору')
    
    title = CharFilter(field_name='title', lookup_expr='icontains', label='Фильтр по названию')
    
    post_type = ChoiceFilter(choices=Post.POST_TYPES)
    
    # categories__name = MultipleChoiceFilter(field_name='categories__name', label='Фильтр по категориям', 
    #                                         choices=DataProvider.get_categories_names_for_choices())
    
    rating = NumberFilter(field_name='rating', label='Фильтр по рейтингу')
    
    time_create = DateFilter(field_name='time_create', lookup_expr='gte', label='Фильтр по дате')
    
    class Meta():
        model = Post
        fields = [
            'author__user__username',
            'title',
            'post_type',
            # 'categories__name',
            'rating',
            'time_create'
            ]
