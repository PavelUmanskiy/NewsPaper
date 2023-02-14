from django.contrib.auth.mixins import UserPassesTestMixin
import news.models
from datetime import datetime

class LikeMixin():
    def like(self):
        self.rating += 1
        self.save()
    
    def dislike(self):
        self.rating -= 1
        self.save()


class UserIsAuthorOfPostMixin(UserPassesTestMixin):
    def test_func(self) -> bool:
        user_author_id = news.models.Author.objects.get(user__pk=self.request.user.pk).id
        post_author_id = news.models.Post.objects.get(pk=self.kwargs['pk']).author_id
        return user_author_id == post_author_id


class UserIsOwnerOfProfileMixin(UserPassesTestMixin):
    def test_func(self) -> bool:
        user_id = news.models.User.objects.get(pk=self.request.user.pk).id
        profile_user_id = news.models.User.objects.get(pk=self.kwargs['pk']).id
        return user_id == profile_user_id


def my_HTTP_request_console_log(request) -> None:
    print(
        '#' * 71 + '\n',
        datetime.now(),
        request,
        request.user,
        '\n' + '#' * 71 + '\n',
        request.session.items(),
        '\n' + '#' * 71 + '\n'
        )
    return None


def email_recipient_list_constructor(author: tuple, categories_id: tuple) -> list:
    """Функция создаёт список получателей писем, основываясь на подписках
    пользователей, категориях и авторстве поста. Можно использовать где
    угодно при условии что переданы правильные аргументы.

    Args:
        author (tuple): кортеж id авторов
        categories_id (tuple): кортеж с перечнем id категорий поста

    Returns:
        list: список email подходящих подписчиков, каждый email - строка
    """
    if not author:
        return []
    elif len(author) == 1:
        author = str((0, author[0]))
    else:
        author = str(author)
    
    if not categories_id:
        return []
    elif len(categories_id) == 1:
        categories_id = str((0, categories_id[0]))
    else:
        categories_id = str(categories_id)
            
    subscribers_iterator = news.models.User.objects.raw(
        """
        SELECT
            au.id,
            au.email
        FROM
            auth_user AS au
        JOIN
            news_subscriber AS ns
                ON ns.user_id = au.id
        JOIN
            news_subscribercategory AS nsc
                ON ns.id = nsc.subscriber_id
        JOIN
            news_subscriberauthor AS nsa
                ON nsa.subscriber_id = ns.id
        WHERE
            nsa.author_id IN """ + author +
        """
        INTERSECT
        SELECT
            au.id,
            au.email
        FROM
            auth_user AS au
        JOIN
            news_subscriber AS ns
                ON ns.user_id = au.id
        JOIN
            news_category AS nc
                ON nc.id IN """ + categories_id +
        """
        JOIN
            news_subscriberauthor AS nsa
            ON nsa.subscriber_id = ns.id
        WHERE
            nsa.author_id IN """ + author
)
    recipient_list = [subscriber.email for subscriber in subscribers_iterator]
    return recipient_list


def email_info(self, request) -> tuple:
    """Функция получает всю необходимую для отправки email
    информацию из HTTP запроса. Создан для использования в
    методе post класса представления PostCreate.

    Args:
        self: инстанс класса PostCreate
        request: инстанс класса HttpRequest
    Returns:
        tuple: Содержит имя автора, строку с именем категорий и список получателей
    """    
    author = str(news.models.Author.objects.get(user_id=self.request.user.id).id)
    categories_list = request._post.getlist('categories', 0)
    if len(categories_list) == 1:
        categories_id = (0, int(categories_list[0]))
    else:
        categories_id = tuple(map(int, categories_list))
    categories_names = ''
    for category_id in categories_id:
        if not category_id:
            continue
        categories_names += news.models.Category.objects.filter(pk=category_id).values_list('name')[0][0] + ' '
    categories_id = str(categories_id)
    recipient_list = email_recipient_list_constructor(author, categories_id)
    author_name = news.models.Author.objects.get(pk=author)
    return (author_name, categories_names, recipient_list)