from .models import Person, Colour, City, Hobby
from django.contrib.auth.models import User
from django.utils.timezone import now
from rest_framework import serializers
from rest_framework.settings import api_settings

class RegisterSerializer(serializers.Serializer):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other')
    ]
    
    HOBBY_CHOICES = [
        ('Sports', 'Sports'),
        ('Reading', 'Reading'),
        ('Music', 'Music'),
        ('Gaming', 'Gaming'),
        ('Traveling', 'Traveling')
    ]

    username = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    gender = serializers.ChoiceField(choices=GENDER_CHOICES)  # Single choice
    hobbies = serializers.MultipleChoiceField(choices=HOBBY_CHOICES, required=False)  # Multiple choices
    current_time = serializers.TimeField(format=api_settings.TIME_FORMAT, input_formats=None, default=now().time)
    registered_at = serializers.DateTimeField(format=api_settings.DATETIME_FORMAT, input_formats=None, default=now)

    def validate(self, data):
        if User.objects.filter(username=data['username']).exists():
            raise serializers.ValidationError({"username": "Username already exists"})
        
        if User.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError({"email": "Email already exists"})

        return data

    def create(self, validated_data):
        validated_data.pop('current_time', None)  # Remove non-user fields
        validated_data.pop('registered_at', None)
        validated_data.pop('hobbies', None)  # Remove extra fields not needed for user creation

        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email']
        )
        user.set_password(validated_data['password'])
        user.save()
        return validated_data

class LoginSerializer(serializers.Serializer):
    username=serializers.CharField()
    password=serializers.CharField()

class ColourSerializer(serializers.ModelSerializer):
    class Meta:
        model=Colour
        fields = ('name', 'id')

class HobbySerializer(serializers.ModelSerializer):
    class Meta:
        model = Hobby
        fields = ('name', 'id')


class CitySerializer(serializers.ModelSerializer):
    max_age = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = City
        fields = ('id', 'name', 'state', 'country', 'max_age')

class PeopleSerializer(serializers.ModelSerializer):
    # hobby_count = serializers.IntegerField(read_only=True)
    # city_name = serializers.StringRelatedField(source='city', read_only=True)
    # color_id = serializers.PrimaryKeyRelatedField(queryset=Colour.objects.all())
    # hobby_slugs = serializers.SlugRelatedField(many=True, read_only=True, slug_field='name')
    # city_url = serializers.HyperlinkedRelatedField(view_name='city-detail', read_only=True, source='city')
    # person_url = serializers.HyperlinkedIdentityField(view_name='person-detail')
    # colour_info = serializers.SerializerMethodField()
 
    class Meta:
        model=Person
        fields = ('hobbies', 'id', 'name', 'age', 'email', 'phone', 'gender')
        # exclude = [' name' , 'age ']  we don't want to add it
        # fields = '__all__'
        depth = 1

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