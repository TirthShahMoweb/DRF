from rest_framework import serializers
from home.models import Person, Colour

class PeopleSerializer(serializers.ModelSerializer):
    hobby_count = serializers.IntegerField(read_only=True)
    # city_name = serializers.StringRelatedField(source='City', read_only=True)
    # color_id = serializers.PrimaryKeyRelatedField(queryset=Colour.objects.all())
    hobby_slugs = serializers.SlugRelatedField(many=True, read_only=True, slug_field='name')
    # city_url = serializers.HyperlinkedRelatedField(view_name='city-detail', read_only=True, source='city')
    # person_url = serializers.HyperlinkedIdentityField(view_name='person-detail')
    # colour_info = serializers.SerializerMethodField()
    # category = serializers.CharField()
    # status = serializers.CharField()
    # primary_contact = serializers.CharField()

    class Meta:
        model=Person
        fields = ('hobby_slugs', 'name', 'age', 'color', 'hobbies', 'id', 'hobby_count')
        # exclude = [' name' , 'age ']  we don't want to add it
        # fields = '__all__'
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