from django.db import models
from django.dispatch import receiver

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

import uuid
import os


class User(models.Model):
    GENDER_CHOICES = [
        (0, 'Not Specified'),
        (1, 'Male'),
        (2, 'Female')
    ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    push_notification_id = models.CharField(max_length=50, null=True, blank=True)
    wallet_address = models.CharField(max_length=42, null=True, blank=True)
    referral_code = models.UUIDField(default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=50, null=True, blank=True)
    last_name = models.CharField(max_length=50, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)
    birthdate = models.DateField()
    gender = models.IntegerField()
    active = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email
    


@receiver(models.signals.post_save, sender=User)
def send_user_email(sender, instance, created, *args, **kwargs):
    if created:
        sendgrid_key = os.environ.get('SENDGRID_KEY')

        email_content = f'Hello, {instance.first_name}! You have registered as a user on Rentals.com. Welcome :)'

        message = Mail(
            from_email='hey@rentals.com',
            to_emails=instance.email,
            subject='Welcome to Rentals.com',
            html_content=email_content)

        try:
            email = SendGridAPIClient(sendgrid_key)
            response = email.send(message)
        except Exception:
            print('Could not send email.')


class Token(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)


@receiver(models.signals.post_save, sender=Token)
def send_token_email(sender, instance, created, *args, **kwargs):
    if created:
        sendgrid_key = os.environ.get('SENDGRID_KEY')

        email_content = f'Hello, {instance.user.first_name}! Use token '  + str(instance.token) + ' to log into the Rentals.com app.'

        message = Mail(
            from_email='token@rentals.com',
            to_emails=instance.user.email,
            subject='Rentals.com Login Token: '  + str(instance.token),
            html_content=email_content)

        try:
            email = SendGridAPIClient(sendgrid_key)
            response = email.send(message)
        except Exception:
            print('Could not send email.')


class Search(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    filters = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
