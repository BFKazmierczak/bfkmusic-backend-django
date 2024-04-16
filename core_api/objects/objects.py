import graphene
from graphene_django import DjangoObjectType

from core_api.models import Audio, Comment, Song, UserLibrary
from django.contrib.auth.models import User


class AudioType(DjangoObjectType):
    class Meta:
        model = Audio
        interfaces = (graphene.relay.Node,)


class SongType(DjangoObjectType):
    class Meta:
        model = Song
        interfaces = (graphene.relay.Node,)

    audio_files = graphene.List("core_api.objects.objects.AudioType")
    comments = graphene.List("core_api.objects.objects.CommentType")

    def resolve_audio_files(self, info):
        return self.audio_files.all()

    def resolve_comments(self, info):
        return self.comments.all()


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
