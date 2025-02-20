from django.contrib import admin
from .models import Colour, Person, City, Hobby
# Register your models here.


admin.site.register(Colour)
admin.site.register(Person)
admin.site.register(City)
admin.site.register(Hobby)
