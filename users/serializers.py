from rest_framework.serializers import ModelSerializer
from properties.models import PropertyType, Property, Plan, Area, AreaImage, Showing
from users.models import User, Search

class UserSerializer(ModelSerializer):
    class PropertySerializer(ModelSerializer):
        class PlanSerializer(ModelSerializer):
            class Meta:
                model = Plan
                exclude = ['property']

        class AreaSerializer(ModelSerializer):
            class AreaImageSerializer(ModelSerializer):
                class Meta:
                    model = AreaImage
                    exclude = ['area']

            images = AreaImageSerializer(source='areaimage_set', many=True)

            class Meta:
                model = Area
                exclude = ['property']
                depth = 1

        plans = PlanSerializer(source='plan_set', many=True)
        areas = AreaSerializer(source='area_set', many=True)

        class Meta:
            model = Property
            exclude = ['creator']
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
            fields = '__all__'

    owned_properties = PropertySerializer(source='creator', many=True)
    managed_properties = PropertySerializer(source='manager', many=True)
    realtor_showings = ShowingSerializer(source='realtor', many=True)
    client_showings = ShowingSerializer(source='client', many=True)

    class Meta:
        model = User
        fields = '__all__'


class SearchSerializer(ModelSerializer):
    class Meta:
        model = Search
        fields = '__all__'
        depth = 1