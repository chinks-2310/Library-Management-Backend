import graphene
from .query import Query as bookQuery
from .mutation import Mutation as bookMutation


class Query(bookQuery, graphene.ObjectType):
    pass


class Mutation(bookMutation, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
