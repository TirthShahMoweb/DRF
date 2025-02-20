from django.utils import timezone
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver

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
    color = models.ForeignKey(Colour, null=True, blank=True, on_delete=models.CASCADE, related_name="color")
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True, null=True)
    hobbies = models.ManyToManyField(Hobby, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name

@receiver(pre_save, sender=Person)
def update_person(sender, instance, **kwargs):
    '''
    This function will update the updated_at field of the Person model
    whenever the is_active field is not updated.
    '''
    person = Person.objects.filter(pk=instance.pk).values("is_active").first()
    if person["is_active"] == instance.is_active:
        instance.updated_at = timezone.now()