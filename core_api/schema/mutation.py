import graphene

from core_api.objects.mutations import (
    SongAddToFavorites,
    SongCreate,
    UserLogin,
    UserLogout,
    UserRegister,
)


class Mutation(graphene.ObjectType):
    song_create = SongCreate.Field()
    song_add_to_favorites = SongAddToFavorites.Field()
    user_register = UserRegister.Field()
    user_login = UserLogin.Field()
    user_logout = UserLogout.Field()
