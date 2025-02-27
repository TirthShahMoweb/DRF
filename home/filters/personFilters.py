import django_filters
from home.models import Person

class PersonFilter(django_filters.FilterSet):
    class Meta:
        model = Person
        fields = {
            'name': ['iexact', 'icontains'],
            'age': ['exact', 'lt', 'gt', 'range'],
        }