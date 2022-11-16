from django.db import models
from users.models import User
from properties.models import Property
from django.dispatch import receiver

import uuid

class Message(models.Model):
    MESSAGE_STATUS= [
        (0, 'Sent'),
        (1, 'Delivered'),
        (2, 'Read')
    ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    message = models.CharField(max_length=250, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField()
    reference_msg = models.ForeignKey('self', on_delete=models.PROTECT, related_name='reference', null=True)
    sender = models.ForeignKey(User, on_delete=models.PROTECT, related_name='sender')
    recipient = models.ForeignKey(User, on_delete=models.PROTECT, related_name='recipient')

    def __str__(self):
        return self.name

class Attachment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    file = models.Field()
    message = models.ForeignKey(Message, on_delete=models.PROTECT, related_name='attach', null=True)
    

class PropertyMessage(Message):
    property = models.ForeignKey(Property, on_delete=models.PROTECT, related_name='property')
