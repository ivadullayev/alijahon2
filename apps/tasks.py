from time import time

from celery import shared_task
from django.core.mail import EmailMessage, send_mail

from root.settings import EMAIL_HOST_USER


# @shared_task
# def send_to_email_task(subject, message, email):
#     email_message = EmailMessage(subject, message, to=[email])
#     email_message.content_subtype = 'html'
#     email_message.send()
#     return {'status': 'yuborildi', "email": email}


# @shared_task
# def send_to_email_task(subject, message, email):
#     email = EmailMessage(subject, message, to=[email])
#     email.content_subtype = 'html'
#     email.send()
#
#     return {'status': 'yuborildi', "email": email}

@shared_task
def send_to_email(msg, email):
    subject = "Django tema"  # noqa

    if not msg:
        msg = 'ushbu xabar Alijahon proyektimdan yuborildi '  # noqa
    start = time()
    send_mail(subject, msg, EMAIL_HOST_USER, [email])
    end = time()

    return {'status': 'yuborildi', 'time': f"{int(end - start)} s", "email": email}
