import json
from django.db.models.signals import post_save
from django.dispatch import receiver

from core_api.audio_processing.waveform_extractor import extract_peaks
from core_api.models import Audio

from django.conf import settings

from django.db.models.fields.files import FieldFile


@receiver(post_save, sender=Audio)
def process_audio(sender, instance: Audio, created, **kwargs):
    if created:
        file: FieldFile = instance.file

        amplitudes, duration = extract_peaks(file.path)

        json_amplitudes = json.dumps(amplitudes)

        instance.waveform = json_amplitudes
        instance.duration = duration
        instance.save()
