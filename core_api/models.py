from django.db import models
from django.contrib.auth.models import User


class TimeStampModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Audio(TimeStampModel):
    uploaded_by = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, default=None
    )
    name = models.CharField(blank=True, max_length=60)
    description = models.CharField(max_length=500, null=True, default=None, blank=True)
    duration = models.FloatField(null=True, blank=True, default=None)
    waveform = models.JSONField(null=True, blank=True, default=None)
    file = models.FileField(upload_to="songs/")
    song = models.ForeignKey(
        "core_api.Song",
        related_name="audio_files",
        blank=True,
        null=True,
        default=None,
        on_delete=models.CASCADE,
    )


class Song(TimeStampModel):
    class Meta:
        ordering = ["published_at"]
        permissions = [("add_to_favorites", "Can add a song to favorites")]

    published_at = models.DateTimeField(default=None)
    name = models.CharField(max_length=128)
    description = models.CharField(max_length=500, default=None)
    non_owner_visible = models.BooleanField(default=True)


class Comment(TimeStampModel):
    content = models.CharField(max_length=1000)
    user = models.ForeignKey(User, related_name="comments", on_delete=models.DO_NOTHING)
    start_time = models.IntegerField()
    end_time = models.IntegerField()
    song = models.ForeignKey(Song, related_name="comments", on_delete=models.DO_NOTHING)
    audio = models.ForeignKey(
        Audio, related_name="comments", on_delete=models.DO_NOTHING
    )


class UserLibrary(models.Model):
    class Meta:
        verbose_name_plural = "User libraries"

    songs = models.ManyToManyField(Song, related_name="libraries", blank=True)
    user = models.OneToOneField(User, related_name="library", on_delete=models.CASCADE)


class UserFavorite(models.Model):
    user = models.ForeignKey(User, related_name="favorites", on_delete=models.CASCADE)
    song = models.ForeignKey(
        Song, related_name="favorited_by", on_delete=models.CASCADE
    )
