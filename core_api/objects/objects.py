import graphene
from graphene_django import DjangoObjectType

from core_api.models import Audio, Comment, Song, UserLibrary
from django.contrib.auth.models import User

from core_api.utils.utils import song_in_library


class AudioType(DjangoObjectType):
    class Meta:
        model = Audio
        interfaces = (graphene.relay.Node,)

    comments = graphene.List("core_api.objects.objects.CommentType")

    def resolve_comments(self, info):
        user = info.context.user

        print(self.song)

        if not song_in_library(user, self.song.id):
            return []

        return self.comments.all()


class SongType(DjangoObjectType):
    class Meta:
        model = Song
        interfaces = (graphene.relay.Node,)
        exclude = ("comments",)

    audio_files = graphene.List("core_api.objects.objects.AudioType")
    in_library = graphene.Boolean()
    is_favorite = graphene.Boolean()

    def resolve_audio_files(self, info):
        user = info.context.user

        if song_in_library(user, self.id) is False:
            return [self.audio_files.order_by("created_at").first()]

        return self.audio_files.order_by("-created_at").all()

    def resolve_in_library(self, info):
        user = info.context.user

        return song_in_library(user, self.id)

    def resolve_is_favorite(self, info):
        user = info.context.user

        if not user.is_authenticated:
            return False

        return self.favorited_by.filter(user_id=user.id).exists()


class CommentType(DjangoObjectType):
    class Meta:
        model = Comment
        interfaces = (graphene.relay.Node,)


class UserType(DjangoObjectType):
    class Meta:
        model = User
        only_fields = ("id", "username", "first_name", "last_name", "email")


class UserLibraryType(DjangoObjectType):
    class Meta:
        model = UserLibrary
        interfaces = (graphene.relay.Node,)
