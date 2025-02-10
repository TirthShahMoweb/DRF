from django.db import models

class Colour(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Person(models.Model):
    color = models.ForeignKey(Colour, null=True, blank=True, on_delete=models.CASCADE, related_name="color")
    name=models.CharField(max_length=50)
    age=models.IntegerField()