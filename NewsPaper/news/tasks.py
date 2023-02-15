from celery import shared_task
from datetime import datetime, timedelta
import time

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from NewsPaper.settings import DEFAULT_FROM_EMAIL
import news.models
from news.utils import email_recipient_list_constructor

@shared_task
def celery_send_multialternatives(subject: str, body: str, from_email: str, 
                                  to: list, attach: tuple) -> None:
    message = EmailMultiAlternatives(
    subject=subject,
    body=body,
    from_email=from_email,
    to=to)
    message.attach_alternative(attach[0], attach[1])
    message.send()
    

@shared_task
def celery_weekly_notifications():
    for subscriber in news.models.Subscriber.objects.all():
        subscriber_categories = tuple(
            [dict_['id'] for dict_ in subscriber.categories.all().values('id')])
        subscriber_authors = tuple(
            [dict_['id'] for dict_ in subscriber.authors.all().values('id')])
        recipient_list = email_recipient_list_constructor(
            subscriber_authors, subscriber_categories)
        
        today = datetime.now()
        week = timedelta(days=7)
        last_week = today - week
        
        new_posts = news.models.Post.objects.filter(
            categories__in=subscriber_categories,
            time_create__gte=last_week.strftime("%Y-%m-%d %H:%M:%S.%f"))
        
        html_content = render_to_string(
            'mesages/weekly_news.html',
            {
                'posts': new_posts,
                'subscriber': subscriber.user.username,
            }
        )
        
        message = EmailMultiAlternatives(
            subject='Всё новое за прошедшую неделю',
            body='',
            from_email=DEFAULT_FROM_EMAIL,
            to=recipient_list
        )
        message.attach_alternative(html_content, 'text/html')
        message.send() 