from django.db.models import Max, Count
from rest_framework.generics import ListCreateAPIView
from ..models import City
from ..serializers.CitySerializers import CitySerializer

class ListCreatePerson(ListCreateAPIView):
    '''
        Create or List person
    '''
    serializer_class = CitySerializer
    queryset = City.objects.all()\
    .annotate(max_age=Max('city_person__age')) \
    .filter(max_age__isnull = False)
    
    # queryset = City.objects.annotate(max_age=Max('city_person__age')).filter(max_age__isnull=False)
    # queryset = City.objects.annotate(max_age=Count('city_person')).filter(max_age__gt=0).order_by('max_age')
