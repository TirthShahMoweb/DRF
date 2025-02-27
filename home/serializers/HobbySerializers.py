from rest_framework import serializers
from home.models import Hobby

class HobbySerializer(serializers.ModelSerializer):
    class Meta:
        model = Hobby
        fields = ('name', 'id')
