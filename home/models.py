from django.utils import timezone
from django.db import models
from .managers.personManager import PesonManager


class Colour(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class City(models.Model):
    name = models.CharField(max_length=100, unique=True, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.name
    
class Hobby(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.name

class Person(models.Model):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    )
    name = models.CharField(max_length=50)
    age = models.IntegerField()
    email = models.EmailField(unique=True, blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, blank=True, related_name="city_person")
    color = models.ForeignKey(Colour, on_delete=models.CASCADE, null=True, blank=True, related_name="color")
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True, null=True)
    hobbies = models.ManyToManyField(Hobby, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    objects = PesonManager()
    admin_objects = models.Manager()

    def __str__(self):
        return self.name