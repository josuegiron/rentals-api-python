from rest_framework.serializers import ModelSerializer
from properties.models import PropertyType, Property, Plan, Area, AreaImage, Showing, AreaReservation
from users.models import User


class PropertySerializer(ModelSerializer):
    class UserSerializer(ModelSerializer):
        class Meta:
            model = User
            fields = ['id', 'first_name', 'last_name']

    class PlanSerializer(ModelSerializer):
        class Meta:
            model = Plan
            exclude = ['property']

    class AreaSerializer(ModelSerializer):
        class AreaImageSerializer(ModelSerializer):
            class Meta:
                model = AreaImage
                exclude = ['area']

        class AreaReservationSerializer(ModelSerializer):
            class Meta:
                model = AreaReservation
                exclude = ['area']

        images = AreaImageSerializer(source='areaimage_set', many=True)
        reservations = AreaReservationSerializer(source='reservation_set', many=True)

        class Meta:
            model = Area
            exclude = ['property']
            depth = 1

    class ShowingSerializer(ModelSerializer):
        class UserSerializer(ModelSerializer):
            class Meta:
                model = User
                fields = ['id', 'first_name', 'last_name']

        realtor = UserSerializer()
        client = UserSerializer()

        class Meta:
            model = Showing
            exclude = ['property']

    managers = UserSerializer(many=True)
    plans = PlanSerializer(source='plan_set', many=True)
    areas = AreaSerializer(source='area_set', many=True)
    showings = ShowingSerializer(source='showing_set', many=True)

    class Meta:
        model = Property
        fields = '__all__'
