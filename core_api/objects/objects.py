import graphene
from graphene_django import DjangoObjectType

from core_api.models import Audio, Comment, Song
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


class CommentType(DjangoObjectType):
    class Meta:
        model = Comment
        interfaces = (graphene.relay.Node,)


class UserType(DjangoObjectType):
    class Meta:
        model = User
        only_fields = ("id", "username", "first_name", "last_name", "email")
