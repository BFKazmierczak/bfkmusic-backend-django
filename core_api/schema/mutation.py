import graphene

from core_api.objects.mutations import (
    CommentCreate,
    SongAddToFavorites,
    SongCreate,
    SongUploadVersion,
    UserLogin,
    UserLogout,
    UserRegister,
)


class Mutation(graphene.ObjectType):
    song_create = SongCreate.Field()
    song_add_to_favorites = SongAddToFavorites.Field()
    audio_upload_version = SongUploadVersion.Field()
    comment_create = CommentCreate.Field()
    user_register = UserRegister.Field()
    user_login = UserLogin.Field()
    user_logout = UserLogout.Field()
