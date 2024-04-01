import graphene

from core_api.objects.mutations import SongCreate, UserRegister


class Mutation(graphene.ObjectType):
    song_create = SongCreate.Field()
    user_register = UserRegister.Field()
