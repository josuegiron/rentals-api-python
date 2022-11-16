from rest_framework.serializers import ModelSerializer
from properties.models import PropertyType, Property, Plan, AreaType, Amenity, Area, AreaImage, Showing, AreaReservation


class PropertyTypeSerializer(ModelSerializer):
    class Meta:
        model = PropertyType
        fields = '__all__'


class PropertySerializer(ModelSerializer):
    class Meta:
        model = Property
        fields = '__all__'


class PlanSerializer(ModelSerializer):
    class Meta:
        model = Plan
        fields = '__all__'


class AreaTypeSerializer(ModelSerializer):
    class Meta:
        model = AreaType
        fields = '__all__'


class AmenitySerializer(ModelSerializer):
    class Meta:
        model = Amenity
        fields = '__all__'


class AreaSerializer(ModelSerializer):
    class Meta:
        model = Area
        fields = '__all__'


class AreaImageSerializer(ModelSerializer):
    class Meta:
        model = AreaImage
        fields = '__all__'


class AreaReservationSerializer(ModelSerializer):
    class Meta:
        model = AreaReservation
        fields = '__all__'


class ShowingSerializer(ModelSerializer):
    class Meta:
        model = Showing
        fields = '__all__'

