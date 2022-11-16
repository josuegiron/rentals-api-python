from rest_framework.viewsets import ModelViewSet
from inbox.models import Message, Attachment
from inbox import basic_serializers, serializers

import os
import jwt
import json


# Create your views here.
def authorize(request):
    jwt_key = os.environ.get('JWT_KEY')

    try:
        authorization_token = request.headers['Authorization']
    except KeyError:
        return None

    try:
        user = jwt.decode(authorization_token, jwt_secret_key, algorithms=["HS256"])
    except jwt.DecodeError or jwt.InvalidSignatureError:
        return None

    return user['id']


class MessageView(ModelViewSet):
    def get_queryset(self):
        authorized_user = authorize(self.request)
        return Message.objects.filter(message__sender=authorized_user)

    serializer_class = serializers.MessageSerializer


class AttachmentView(ModelViewSet):
    queryset = Attachment.objects.all()
    serializer_class = basic_serializers.AttachmentSerializer


class PropertyMessageView(ModelViewSet):
    def get_queryset(self):
        authorized_user = authorize(self.request)
        return Message.objects.filter(property_message__sender=authorized_user, property_message__property=property)

    serializer_class = serializers.PropertyMessageSerializer
