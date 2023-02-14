import logging
from datetime import datetime, timedelta
 
from django.conf import settings
from django.core.management.base import BaseCommand
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
 
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution


from NewsPaper.settings import DEFAULT_FROM_EMAIL

import news.models
from news.utils import email_recipient_list_constructor
 
logger = logging.getLogger(__name__)
 
 
# наша задача по выводу текста на экран
def my_job():
    #  Your job processing logic here... 
    print('Job inialized...')
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
 
# функция, которая будет удалять неактуальные задачи
def delete_old_job_executions(max_age=604_800):
    """This job deletes all apscheduler job executions older than `max_age` from the database."""
    DjangoJobExecution.objects.delete_old_job_executions(max_age)
 
 
class Command(BaseCommand):
    help = "Runs apscheduler."
 
    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")
        
        # добавляем работу нашему задачнику
        scheduler.add_job(
            my_job,
            trigger=CronTrigger(hour=9, day_of_week=1),
            id="my_job",  # уникальный айди
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'my_job'.")
 
        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),  # Каждую неделю будут удаляться старые задачи, которые либо не удалось выполнить, либо уже выполнять не надо.
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info(
            "Added weekly job: 'delete_old_job_executions'."
        )
 
        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")