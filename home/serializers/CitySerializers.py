from rest_framework import serializers
from home.models import City

class CitySerializer(serializers.ModelSerializer):
    max_age = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = City
        fields = ('id', 'name', 'state', 'country', 'max_age')