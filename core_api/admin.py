from django.contrib import admin
from .models import Audio, Comment, Song


class AudioInline(admin.TabularInline):
    model = Audio
    extra = 0


@admin.register(Song)
class SongAdmin(admin.ModelAdmin):
    inlines = [AudioInline]


admin.site.register(Audio)
admin.site.register(Comment)
