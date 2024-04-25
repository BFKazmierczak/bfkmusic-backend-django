from django.db import models
from django.contrib.auth.models import User


class Audio(models.Model):
    duration = models.FloatField(default=None)
    waveform = models.JSONField(default=None)
    file = models.FileField(upload_to="songs/")
    song = models.ForeignKey(
        "core_api.Song",
        related_name="audio_files",
        blank=True,
        null=True,
        default=None,
        on_delete=models.CASCADE,
    )


class Song(models.Model):
    class Meta:
        ordering = ["published_at"]
        permissions = [("add_to_favorites", "Can add a song to favorites")]

    published_at = models.DateField()
    name = models.CharField(max_length=128)
    description = models.CharField(max_length=500, default=None)
    non_owner_visible = models.BooleanField(default=True)

    @property
    def is_favorite(self):
        return self.favorited_by.exists()


class Comment(models.Model):
    content = models.CharField(max_length=1000)
    user = models.ForeignKey(User, related_name="comments", on_delete=models.CASCADE)
    time_range = models.CharField(max_length=50)
    song = models.ForeignKey(Song, related_name="comments", on_delete=models.CASCADE)


class UserLibrary(models.Model):
    class Meta:
        verbose_name_plural = "User libraries"

    songs = models.ManyToManyField(Song, blank=True)
    user = models.OneToOneField(User, related_name="library", on_delete=models.CASCADE)


class UserFavorite(models.Model):
    user = models.ForeignKey(User, related_name="favorites", on_delete=models.CASCADE)
    song = models.ForeignKey(
        Song, related_name="favorited_by", on_delete=models.CASCADE
    )
