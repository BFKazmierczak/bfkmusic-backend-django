import graphene
from graphene_django import DjangoObjectType

from core_api.models import Audio, Song


class AudioType(DjangoObjectType):
    class Meta:
        model = Audio
        interfaces = (graphene.relay.Node,)


class SongType(DjangoObjectType):
    class Meta:
        model = Song
        interfaces = (graphene.relay.Node,)
