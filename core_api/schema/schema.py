import graphene
from core_api.schema.mutation import Mutation
from core_api.schema.query import Query


schema = graphene.Schema(query=Query, mutation=Mutation)
