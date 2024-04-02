from django.db import models


class Audio(models.Model):
    duration = models.FloatField()
    waveform = models.JSONField()
    file = models.FileField(upload_to="songs/")


class Song(models.Model):
    class Meta:
        permissions = [("create_song", "Can create a song")]

    name = models.CharField(max_length=128)
    published_at = models.DateField()
    audio_files = models.ManyToManyField(Audio)
