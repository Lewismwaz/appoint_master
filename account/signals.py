from django.db.models.signals import post_delete
from django.dispatch import receiver
from .models import User, ID


# This signal is triggered when a registered user is deleted. 
# It updates the registered field of the ID record associated with the user(from registered to unregistered).
@receiver(post_delete, sender=User)
def user_deleted(instance, **kwargs):
    try:
        id_record = ID.objects.get(patient_id=instance.patient_id)
        id_record.registered = False
        id_record.save()
    except ID.DoesNotExist:
        pass