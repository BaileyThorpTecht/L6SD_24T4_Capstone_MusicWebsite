from celery import shared_task
from django.contrib.auth.models import User
from django.core.mail import EmailMessage, send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from itertools import islice
import logging

logger = logging.getLogger(__name__)

"""This is for handling high-traffic when dealing with multiple users"""

# Helper function to batch user queryset into chunks
def batch_queryset(queryset, batch_size=100):
    for x in range(0, queryset.count(), batch_size):
        yield queryset[x:x + batch_size]



"""This is for daily notifications"""

# Task to send daily emails in batches
@shared_task
def send_daily_email():
    """Sends a daily reminder to all registered users encouraging them to continue their skill development"""
    users = User.objects.all()
    if users.exists():
        for user_batch in batch_queryset(users, batch_size=100):  # Send in batches
            for user in user_batch:
                try:
                    context = {'username': user.username}
                    subject = '🎵 Reminder: Your Daily Music Practice Awaits!'
                    email_body = render_to_string("users/daily_email_template.html", context)

                    email = EmailMultiAlternatives(
                        subject,
                        email_body,
                        settings.EMAIL_HOST_USER,
                        [user.email]
                    )
                    email.attach_alternative(email_body, "text/html")
                    email.send(fail_silently=False)
                    logger.info(f"Email sent successfully to {user.email}")
                except Exception as e:
                    logger.error(f"Failed to send email to {user.email}: {e}")
    else:
        logger.error("No users found to send reminders.")


# Task to send emails to a batch of users
# @shared_task
# def send_daily_reminders():
#     """Sends a daily reminder to all registered users in batches"""
#     users = User.objects.all()
#     if users.exists():
#         for user_batch in batch_queryset(users, batch_size=100):
#             for user in user_batch:
#                 try:
#                     context = {'username': user.username}
#                     subject = '🎵 Reminder: Your Daily Music Practice Awaits!'
#                     email_body = render_to_string("users/daily_email_template.html", context)
                    
#                     email = EmailMultiAlternatives(
#                         subject,
#                         email_body,
#                         settings.EMAIL_HOST_USER,
#                         [user.email]
#                     )
                    
#                     email.attach_alternative(email_body, "text/html")
#                     email.send(fail_silently=False)
#                 except Exception as e:
#                     print(f"Failed to send email to {user.email}: {e}")
#     else:
#         print("No users found to send reminders.")


"""This is for authenticating email. When usrs register, they are given this"""

# Task to send emails to users when they register
@shared_task
def send_registration_confirmation(user_id):
    """Sends an email confirmation link to the new user after registration"""
    try:
        user = User.objects.get(id=user_id)
        context = {'username' : user.username}
        subject = "Confirm Your Email"
        email_body = render_to_string("users/registration_confirmation.html", context)
        
        email = EmailMultiAlternatives(
            subject, 
            email_body,
            settings.EMAIL_HOST_USER,
            [user.email]
        )
        email.send(fail_silently = False)
    except User.DoesNotExist:
        print(f"User with id {user_id} does not exist.")