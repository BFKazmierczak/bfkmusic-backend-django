import graphene

from core_api.objects.mutations import SongCreate


class Mutation(graphene.ObjectType):
    song_create = SongCreate.Field()
