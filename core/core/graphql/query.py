import graphene
from . import types
from . import resolvers


class Query(graphene.ObjectType):
    books = graphene.List(types.BookDetails, resolver=resolvers.BookViewResolver())
    student = graphene.List(types.StudentDetails, resolver=resolvers.StudentViewResolver())
