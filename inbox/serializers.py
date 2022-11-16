from rest_framework.serializers import ModelSerializer
from inbox.models import Message, Attachment, PropertyMessage
from users.models import User


class MessageSerializer(ModelSerializer):
    class AttachmentSerializer(ModelSerializer):
        class Meta:
            model = Attachment 
            exclude = ['message']

    class UserSerializer(ModelSerializer):
        class Meta:
            model = User
            fields = ['id', 'first_name', 'last_name']

    sender = UserSerializer()
    recipient = UserSerializer()
    showings = AttachmentSerializer(source='attachment_set', many=True)

    class Meta:
        model = Message 
        fields = '__all__'


class PropertyMessageSerializer(MessageSerializer):
    class Meta:
        model = PropertyMessage
        fields = '__all__'
