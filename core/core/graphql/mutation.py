import graphene
import logging
import datetime
from ..models import BookDetails, Category, Department

logger = logging.getLogger(__name__)


class AddBookCopy(graphene.Mutation):
    ok = graphene.Boolean()
    message = graphene.String()

    class Arguments:
        book_id = graphene.ID(required=True)

    @staticmethod
    def mutate(self, info, book_id, **kwargs):
        try:
            book = BookDetails.objects.get(id=book_id)
            book.no_of_copies_current = book.no_of_copies_current + 1
            book.save()
            return {"ok": True, "message": "Book copies updated"}
        except book_id.DoesNotExist:
            return {"ok": False, "message": "Book Id is missing"}
        except Exception as e:
            logger.error("Something went wrong! Error = " + str(e))
            return {"ok": False, "message": "Failed to update book copy"}


class AddNewBook(graphene.Mutation):
    ok = graphene.Boolean()
    message = graphene.String()

    class Arguments:
        isbn = graphene.String(required=True)
        title = graphene.String(required=True)
        publication_year = graphene.Int()
        language = graphene.String()
        no_of_actual_copy = graphene.Int()
        no_of_current_copy = graphene.Int()
        publisher = graphene.String(required=True)
        category_id = graphene.ID(required=True)

    @staticmethod
    def mutate(self, info, **kwargs):
        try:
            publication_year = kwargs.get("publication_year") or datetime.date.today().year
            no_of_actual_copies = kwargs.get("no_of_actual_copy") or 0
            no_of_current_copies = kwargs.get("no_of_current_copy") or 0
            category = Category.objects.get(id=kwargs.get("category_id"))
            book = BookDetails(isbn=kwargs.get("isbn"), title=kwargs.get("title"),
                               publication_year=publication_year,
                               language=kwargs.get("language"),
                               no_of_actual_copies=no_of_actual_copies,
                               no_of_copies_current=no_of_current_copies,
                               publisher=kwargs.get("publisher"),
                               category=category)
            book.save()
            return {"ok": True, "message": "Book Created in the database successfully"}
        except Exception as e:
            logger.error(e)
            return {"ok": False, "message": "Something went wrong"}


class AddNewCategory(graphene.Mutation):
    ok = graphene.Boolean()
    message = graphene.String()

    class Arguments:
        category_name = graphene.String(required=True)

    @staticmethod
    def mutate(self, info, **kwargs):
        try:
            new_category = Category(category_name=kwargs.get("category_name"))
            new_category.save()
            return {"ok": True, "message": "Category created successfully"}
        except Exception as e:
            logger.error(e)
            return {"ok": False, "message": "Something went wrong"}


class AddNewDepartment(graphene.Mutation):
    ok = graphene.Boolean()
    message = graphene.String()

    class Arguments:
        department_name = graphene.String(required=True)

    @staticmethod
    def mutate(self, info, **kwargs):
        try:
            new_department = Department(department_name=kwargs.get("department_name"))
            new_department.save()
            return {"ok": True, "message": "Department created successfully"}
        except Exception as e:
            logger.error(e)
            return {"ok": False, "message": "Something went wrong"}


class Mutation(graphene.ObjectType):
    add_book_copy = AddBookCopy.Field()
    add_new_category = AddNewCategory.Field()
    add_new_book = AddNewBook.Field()
    add_new_department = AddNewDepartment.Field()
