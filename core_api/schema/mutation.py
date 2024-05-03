import graphene

from core_api.objects.mutations import (
    CommentCreate,
    SongManageFavorite,
    SongCreate,
    SongUploadVersion,
    UserLogin,
    UserLogout,
    UserRegister,
)


class Mutation(graphene.ObjectType):
    song_create = SongCreate.Field()
    song_manage_favorite = SongManageFavorite.Field()
    audio_upload_version = SongUploadVersion.Field()
    comment_create = CommentCreate.Field()
    user_register = UserRegister.Field()
    user_login = UserLogin.Field()
    user_logout = UserLogout.Field()
