from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string

from NewsPaper.settings import DEFAULT_FROM_EMAIL
from .models import *
from .utils import email_recipient_list_constructor


@receiver(signal=[post_save, m2m_changed], sender=PostCategory)
def notify_subscribers_post(sender, instance, **kwargs):
    categories = Post.objects.get(pk=instance.id).categories.all()
    categories_id = tuple([category.id for category in categories])
    recipient_list = email_recipient_list_constructor(author=(instance.author.id,), categories_id=categories_id)
    if recipient_list:       
        html_content = render_to_string(
            'messages/notify_subscribers.html',
            {
                'post': Post.objects.get(pk=instance.id),
            }
        )
        
        message = EmailMultiAlternatives(
            subject=f'Новый пост в Вашей любимой категории от {instance.author}',
            body='',
            from_email=DEFAULT_FROM_EMAIL,
            to=recipient_list
        )
        message.attach_alternative(html_content, 'text/html')
        message.send() 