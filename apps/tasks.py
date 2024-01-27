from celery import shared_task

from apps.utils import send_email


@shared_task
def task_send_email(subject, message, recipient_list):
    send_email(subject, message, recipient_list)
    return "Sended"
