import graphene
from graphene_django.filter import DjangoFilterConnectionField


from core_api.auth.decorators import auth_required
from core_api.models import Song
from core_api.objects.filters import SongFilter
from core_api.objects.objects import SongType


class Query(graphene.ObjectType):
    all_songs = DjangoFilterConnectionField(SongType, filterset_class=SongFilter)
    favorite_songs = DjangoFilterConnectionField(SongType, filterset_class=SongFilter)

    # def resolve_all_songs(self, info):
    #     print("here")
    #     pass

    @auth_required
    def resolve_favorite_songs(self, info):
        user = info.context.user

        return Song.objects.filter(favorited_by__user_id=user.id)
