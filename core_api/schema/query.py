import graphene
from graphene_django.filter import DjangoFilterConnectionField
from django.db.models import Q


from core_api.auth.decorators import auth_required
from core_api.models import Song, UserLibrary
from core_api.objects.filters import SongFilter
from core_api.objects.objects import SongType
from core_api.utils.error_handling import CustomGraphQLError, ErrorEnum
from core_api.utils.utils import get_object_id


def discard_non_visible_songs(user_id: int):
    user_library_songs = UserLibrary.objects.filter(user_id=user_id).values_list(
        "songs__id", flat=True
    )
    return Q(non_owner_visible=True) | Q(id__in=user_library_songs)


class Query(graphene.ObjectType):
    all_songs = DjangoFilterConnectionField(SongType, filterset_class=SongFilter)
    song = graphene.Field(SongType, song_id=graphene.ID(required=True))
    favorite_songs = DjangoFilterConnectionField(SongType, filterset_class=SongFilter)
    user_library = DjangoFilterConnectionField(SongType, filterset_class=SongFilter)

    def resolve_all_songs(self, info, **kwargs):
        user = info.context.user

        if not user.is_authenticated:
            return Song.objects.filter(non_owner_visible=True)

        query = discard_non_visible_songs(user.id)

        return Song.objects.filter(query)

    def resolve_song(self, info, song_id, **kwargs):
        user = info.context.user

        song_id = get_object_id(song_id)

        song = Song.objects.filter(id=song_id).first()
        if song is not None:
            if (
                not song.libraries.filter(user_id=user.id).exists()
                and song.non_owner_visible is False
            ):
                raise CustomGraphQLError(ErrorEnum.SONG_NO_ACCESS)

        return song

    @auth_required
    def resolve_favorite_songs(self, info, **kwargs):
        user = info.context.user

        query = discard_non_visible_songs(user.id) & Q(favorited_by__user_id=user.id)

        return Song.objects.filter(query)

    @auth_required
    def resolve_user_library(self, info, **kwargs):
        user = info.context.user

        user_library = UserLibrary.objects.filter(user_id=user.id).exists()
        if user_library is False:
            raise CustomGraphQLError(ErrorEnum.NO_LIBRARY)

        return user.library.songs.all()
