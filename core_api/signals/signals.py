from django.db.models.signals import pre_save
from django.dispatch import receiver

from core_api.models import Audio


@receiver(pre_save, sender=Audio)
def process_audio(sender, instance, **kwargs):
    if instance.id is None:
        print("audio created")
