from rest_framework import serializers
from .models import Person, Colour
from django.contrib.auth.models import User

class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField()
    email=serializers.EmailField()
    password=serializers.CharField()

    def validate(self, data):
        if data['username']:
            if User.objects.filter(username=data['username']).exists():
                raise serializers.ValidationError("Username already exists")
            
        if data['email']:
            if User.objects.filter(email=data['email']).exists():
                raise serializers.ValidationError("Email already exists")
        return data

    def create(self, validated_data):
        user = User.objects.create_user(username=validated_data['username'],email=validated_data['email'])
        user.set_password(validated_data['password'])
        user.save()
        return validated_data

class LoginSerializer(serializers.Serializer):
    username=serializers.CharField()
    password=serializers.CharField()

class ColourSerializer(serializers.ModelSerializer):
    class Meta:
        model=Colour
        fields = ['name','id']

class PeopleSerializer(serializers.ModelSerializer):
    # color = ColourSerializer(read_only=True)
    # colour_info = serializers.SerializerMethodField()

    class Meta:
        model=Person
        # fields=['name','age']
        # exclude = [' name' , 'age ']  we don't want to add it
        fields = '__all__'
        # depth = 1

    def get_colour_info(self, obj):
        color_obj = Colour.objects.get(id=obj.color.id)
        return {'Color_name':color_obj.name,"hex_code":"#000000"}

    def validate(self, data):
        special_char = "!@#$%^&*()_+=-}{[]\\|<>?/,"
        for c in data['name']:
            if c in special_char:
                raise serializers.ValidationError("Name cannot contain any speacial Chars")
            # if data['age'] < 18:
        #     raise serializers.ValidationError("Age should be greater than 18")
        return data