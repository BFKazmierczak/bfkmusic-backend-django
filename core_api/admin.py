from django.contrib import admin
from .models import Audio, Comment, Song, UserFavorite, UserLibrary


class UserFavoriteAdmin(admin.ModelAdmin):
    list_display = ("user", "song")


class AudioInline(admin.TabularInline):
    model = Audio
    extra = 0


@admin.register(Song)
class SongAdmin(admin.ModelAdmin):
    inlines = [AudioInline]


admin.site.register(Audio)
admin.site.register(Comment)
admin.site.register(UserFavorite, UserFavoriteAdmin)
admin.site.register(UserLibrary)
