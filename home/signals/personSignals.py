from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils import timezone
from home.models import Person


@receiver(pre_save, sender=Person)
def update_person(sender, instance, **kwargs):
    '''
    This function will update the updated_at field of the Person model
    whenever the is_active field is not updated.
    '''
    person = Person.objects.filter(pk=instance.pk).values("is_active").first()
    if person["is_active"] == instance.is_active:
        instance.updated_at = timezone.now()