from django.contrib import admin
from .models import Audio, Comment, Song, UserFavorite, UserLibrary


class UserFavoriteAdmin(admin.ModelAdmin):
    list_display = ("user", "song")


class UserLibraryAdmin(admin.ModelAdmin):
    filter_horizontal = ("songs",)


class AudioInline(admin.TabularInline):
    model = Audio
    extra = 0


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0


@admin.register(Song)
class SongAdmin(admin.ModelAdmin):
    inlines = [CommentInline, AudioInline]


@admin.register(Audio)
class AudioAdmin(admin.ModelAdmin):
    inlines = [CommentInline]


admin.site.register(Comment)
admin.site.register(UserFavorite, UserFavoriteAdmin)
admin.site.register(UserLibrary, UserLibraryAdmin)
