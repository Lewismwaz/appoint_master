from django.db.models.signals import post_delete
from django.dispatch import receiver
from .models import User, ID

@receiver(post_delete, sender=User)
def user_deleted(sender, instance, **kwargs):
    try:
        id_record = ID.objects.get(patient_id=instance.patient_id)
        id_record.registered = False
        id_record.save()
    except ID.DoesNotExist:
        pass
    
