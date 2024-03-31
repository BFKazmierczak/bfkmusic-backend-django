import graphene
from graphene_django.filter import DjangoFilterConnectionField


from core_api.objects.filters import SongFilter
from core_api.objects.objects import SongType


class Query(graphene.ObjectType):
    all_songs = DjangoFilterConnectionField(SongType, filterset_class=SongFilter)
