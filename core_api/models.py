from django.db import models
from django.contrib.auth.models import User


class Audio(models.Model):
    duration = models.FloatField(default=None)
    waveform = models.JSONField(default=None)
    file = models.FileField(upload_to="songs/")


class Song(models.Model):
    class Meta:
        permissions = [("add_to_library", "Can add a song to library")]

    published_at = models.DateField()
    name = models.CharField(max_length=128)
    description = models.CharField(max_length=500, default=None)
    non_owner_visible = models.BooleanField(default=True)
    audio_files = models.ManyToManyField(Audio)


class Comment(models.Model):
    content = models.CharField(max_length=1000)
    user = models.ForeignKey(User, related_name="comments", on_delete=models.CASCADE)
    time_range = models.CharField(max_length=50)
    song = models.ForeignKey(Song, related_name="comments", on_delete=models.CASCADE)


class UserLibrary(models.Model):
    songs = models.ManyToManyField(Song)
    user = models.OneToOneField(User, related_name="library", on_delete=models.CASCADE)
