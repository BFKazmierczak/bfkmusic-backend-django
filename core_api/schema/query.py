import graphene
from graphene_django.filter import DjangoFilterConnectionField
from django.db.models import Q


from core_api.auth.decorators import auth_required
from core_api.models import Song, UserLibrary
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

        user_library_song_ids = UserLibrary.objects.filter(user=user).values_list(
            "songs__id", flat=True
        )

        query = Q(non_owner_visible=True) | Q(id__in=user_library_song_ids) & Q(
            favorited_by__user_id=user.id
        )

        return Song.objects.filter(query)
