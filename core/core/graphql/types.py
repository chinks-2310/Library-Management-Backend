import graphene
from graphene.types.objecttype import ObjectType


class CategoryDetails(ObjectType):
    category_id = graphene.String()
    category_name = graphene.String()


class BookDetails(ObjectType):
    isbn = graphene.String()
    title = graphene.String()
    publication_year = graphene.Int()
    language = graphene.String()
    no_of_actual_copies = graphene.Int()
    no_of_copies_current = graphene.Int()
    publisher = graphene.String()
    category = graphene.Field(CategoryDetails)


class BorrowerDetails(ObjectType):
    borrowed_from_date = graphene.Date()
    borrowed_to_date = graphene.Date()
    actual_return_date = graphene.Date()
    is_return = graphene.Boolean()
    books = graphene.List(BookDetails)


class StudentDetails(ObjectType):
    student_name = graphene.String()
    gender = graphene.Int()
    date_of_birth = graphene.Date()
    borrower = graphene.Field(BorrowerDetails)
