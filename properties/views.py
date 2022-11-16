from rest_framework.viewsets import ModelViewSet
from properties.models import PropertyType, Property, Plan, AreaType, Amenity, Area, AreaImage, Showing, AreaReservation
from properties import basic_serializers, serializers

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


class PropertyTypeView(ModelViewSet):
    queryset = PropertyType.objects.all()
    serializer_class = basic_serializers.PropertyTypeSerializer


class PropertyView(ModelViewSet):
    def get_queryset(self):
        if self.request.method == 'GET':
            if 'filters' in self.request.headers:
                filters = self.request.headers['filters']
                print(filters)
                filters = json.loads(filters)
                return Property.objects.filter(**filters)
            else:
                return Property.objects.all()
        else:
            authorized_user = authorize(self.request)
            return Property.objects.filter(creator=authorized_user)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return serializers.PropertySerializer
        else:
            return basic_serializers.PropertySerializer


class PlanView(ModelViewSet):
    def get_queryset(self):
        authorized_user = authorize(self.request)
        return Plan.objects.filter(property__creator=authorized_user)

    serializer_class = basic_serializers.PlanSerializer


class AreaTypeView(ModelViewSet):
    queryset = AreaType.objects.all()
    serializer_class = basic_serializers.AreaTypeSerializer


class AmenityView(ModelViewSet):
    queryset = Amenity.objects.all()
    serializer_class = basic_serializers.AmenitySerializer


class AreaView(ModelViewSet):
    def get_queryset(self):
        authorized_user = authorize(self.request)
        return Area.objects.filter(property__creator=authorized_user)

    serializer_class = basic_serializers.AreaSerializer


class AreaImageView(ModelViewSet):
    def get_queryset(self):
        authorized_user = authorize(self.request)
        return AreaImage.objects.filter(area__property__creator=authorized_user)

    serializer_class = basic_serializers.AreaImageSerializer


class AreaReservationView(ModelViewSet):
    def get_queryset(self):
        authorized_user = authorize(self.request)
        return AreaReservation.objects.filter(property__creator=authorized_user)

    serializer_class = basic_serializers.AreaReservationSerializer


class ShowingView(ModelViewSet):
    queryset = Showing.objects.all()
    serializer_class = basic_serializers.ShowingSerializer
