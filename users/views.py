from rest_framework.viewsets import ModelViewSet
from users.models import User, Token, Search
from users import basic_serializers, serializers

from rest_framework.views import APIView, Response
from rest_framework import status

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

import os
import jwt
import random


# Create your views here.
def authorize(request):
    jwt_key = os.environ.get('JWT_KEY')

    try:
        authorization_token = request.headers['Authorization']
    except KeyError:
        return None

    try:
        user = jwt.decode(authorization_token, jwt_key, algorithms=["HS256"])
    except jwt.DecodeError or jwt.InvalidSignatureError:
        return None

    return user['id']


class UserView(ModelViewSet):
    def get_queryset(self):
        authorized_user = authorize(self.request)
        return User.objects.filter(id=authorized_user)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return serializers.UserSerializer
        else:
            return basic_serializers.UserSerializer


class GenerateToken(APIView):
    def post(self, request):
        # Variables
        errors = []

        # Get Staff
        if 'email' in self.request.data:
            try:
                user = User.objects.get(email=self.request.data['email'])
            except User.MultipleObjectsReturned:
                errors.append({'user_error': 'More than one matching user.'})
            except User.DoesNotExist:
                errors.append({'user_error': 'User does not exist.'})

        else:
            if 'email' not in self.request.data:
                errors.append({'key_error': 'Email missing from request.'})

        if len(errors) == 0:

            # Remove any unused tokens.
            unused_tokens = Token.objects.filter(user=user)
            for unused_token in unused_tokens:
                unused_token.delete()

            # Generate login token.
            token = random.randint(100000, 999999)
            new_token = Token(user=user, token=token)
            new_token.save()

            print(token)
        return Response(errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR) if len(errors) != 0 else Response(
            {'message': 'Token generated successfully.'}, status=status.HTTP_201_CREATED)


class LoginUser(APIView):
    def post(self, request):
        # Variables
        errors = []
        jwt_key = os.environ.get('JWT_KEY')

        login_email = self.request.data['email']
        login_token = self.request.data['token']

        # Get Staff
        try:
            user = User.objects.get(email=login_email)
            token = Token.objects.get(token=login_token, user=user)
            serialized_user = serializers.UserSerializer(user).data
            web_token = jwt.encode({"id": str(user.id)}, jwt_key, algorithm="HS256")

        except User.DoesNotExist:
            errors.append({'authentication_error': 'Invalid credentials.'})
        except Token.DoesNotExist:
            errors.append({'authentication_error': 'Invalid credentials.'})

        return Response(errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR) if len(errors) != 0 else Response({'jwt': web_token, 'user': serialized_user}, status=status.HTTP_202_ACCEPTED)

class SearchView(ModelViewSet):
    queryset = Search.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return serializers.SearchSerializer
        else:
            return basic_serializers.SearchSerializer
