import graphene
from graphene_django.filter import DjangoFilterConnectionField
from django.db.models import Q


from core_api.auth.decorators import auth_required
from core_api.models import Song, UserLibrary
from core_api.objects.filters import SongFilter
from core_api.objects.objects import SongType


def discard_non_visible_songs(user_id: int):
    user_library_songs = UserLibrary.objects.filter(user_id=user_id).values_list(
        "songs__id", flat=True
    )
    return Q(non_owner_visible=True) | Q(id__in=user_library_songs)


class Query(graphene.ObjectType):
    all_songs = DjangoFilterConnectionField(SongType, filterset_class=SongFilter)
    favorite_songs = DjangoFilterConnectionField(SongType, filterset_class=SongFilter)
    user_library = DjangoFilterConnectionField(SongType, filterset_class=SongFilter)

    def resolve_all_songs(self, info):
        user = info.context.user

        if not user.is_authenticated:
            return Song.objects.filter(non_owner_visible=True)

        query = discard_non_visible_songs(user.id)

        return Song.objects.filter(query)

    @auth_required
    def resolve_favorite_songs(self, info):
        user = info.context.user

        query = discard_non_visible_songs(user.id) & Q(favorited_by__user_id=user.id)

        return Song.objects.filter(query)

    @auth_required
    def resolve_user_library(self, info, **kwargs):
        user = info.context.user

        user_library = user.library

        return user_library.songs.all()
