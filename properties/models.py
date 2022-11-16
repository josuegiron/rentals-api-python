from django.db import models
from users.models import User
from django.dispatch import receiver

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

import uuid
import os


# Create your models here.
class PropertyType(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    active = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    

class Property(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    creator = models.ForeignKey(User, related_name='creator', on_delete=models.PROTECT)
    name = models.CharField(max_length=100)
    main_image = models.ImageField()
    type = models.ForeignKey(PropertyType, on_delete=models.PROTECT)
    land_area = models.FloatField(null=True)
    construction_area = models.FloatField(null=True)
    asking_price = models.FloatField(null=True, blank=True)
    minimum_contract_length = models.PositiveIntegerField()
    date_available = models.DateField()
    address = models.TextField()
    latitude = models.FloatField()
    longitude = models.FloatField()
    managers = models.ManyToManyField(User, related_name='manager')
    max_commission = models.FloatField(null=True)
    active = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name + ' - ' + self.creator.email


class Plan(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    property = models.ForeignKey(Property, on_delete=models.PROTECT)
    image = models.ImageField()
    active = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.property.name


class AreaType(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    active = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    
class Amenity(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    active = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Area(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50)
    type = models.ForeignKey(AreaType, on_delete=models.PROTECT)
    property = models.ForeignKey(Property, on_delete=models.PROTECT)
    area = models.FloatField(null=True, blank=True)
    amenities = models.ManyToManyField(Amenity, null=True, blank=True)
    shared = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.property.name + ' (' + self.type.name + ')'


class AreaImage(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    area = models.ForeignKey(Area, on_delete=models.PROTECT)
    image = models.ImageField()
    active = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True)


class AreaReservation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    comment = models.CharField(max_length=250, blank=True)
    start_date = models.DateTimeField(blank=False)
    end_date = models.DateTimeField(blank=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    area = models.ForeignKey(Area, on_delete=models.PROTECT)
    responsible = models.ForeignKey(User, on_delete=models.PROTECT, related_name='responsible')

    def __str__(self):
        return self.name


class Showing(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    property = models.ForeignKey(Property, on_delete=models.PROTECT)
    realtor = models.ForeignKey(User, on_delete=models.PROTECT, related_name='realtor')
    client = models.ForeignKey(User, on_delete=models.PROTECT, related_name='client')
    appointment = models.DateTimeField()
    active = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)


@receiver(models.signals.post_save, sender=Showing)
def send_showing_email(sender, instance, created, *args, **kwargs):
    if created:
        sendgrid_key = os.environ.get('SENDGRID_KEY')

        email_content = f'Hello! You have scheduled a showign for {instance.property.name}.'

        message = Mail(
            from_email='showings@rentals.com',
            to_emails=[instance.realtor.email, instance.client.email],
            subject='Scheduled showing through Rentals.com',
            html_content=email_content)

        try:
            email = SendGridAPIClient(sendgrid_key)
            response = email.send(message)
        except Exception:
            print('Could not send email.')
