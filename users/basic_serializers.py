from rest_framework.serializers import ModelSerializer
from users.models import User, Search


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class SearchSerializer(ModelSerializer):
    class Meta:
        model = Search
        fields = '__all__'