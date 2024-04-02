import graphene

from core_api.objects.mutations import SongCreate, UserLogin, UserRegister


class Mutation(graphene.ObjectType):
    song_create = SongCreate.Field()
    user_register = UserRegister.Field()
    user_login = UserLogin.Field()
