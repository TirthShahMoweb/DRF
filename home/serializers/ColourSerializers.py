from rest_framework import serializers
from home.models import Colour

class ColourSerializer(serializers.ModelSerializer):
    class Meta:
        model=Colour
        fields = ('name', 'id')