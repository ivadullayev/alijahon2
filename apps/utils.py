






# from celery import shared_task
# from django.contrib.sites.shortcuts import get_current_site
# from django.template.loader import render_to_string
# from django.utils.encoding import force_bytes
# from django.utils.http import urlsafe_base64_encode
#
# # from .tasks import send_to_email_task
# from .tokens import account_activation_token
#
#
# @shared_task
# def generate_one_time_verification(request, user):
#     current_site = get_current_site(request)
#     email = user.email
#     subject = "Verify Email"
#     message = render_to_string('apps/auth/email.html', {
#         'scheme': request.scheme,
#         'user': user,
#         'domain': current_site.domain,
#         'uid': urlsafe_base64_encode(force_bytes(user.pk)),
#         'token': account_activation_token.make_token(user),
#     })
#
#     send_to_email_task.delay(subject, message, email)
