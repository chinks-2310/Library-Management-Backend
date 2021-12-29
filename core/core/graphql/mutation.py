import graphene
import logging
import datetime
from ..models import BookDetails, Category, Department, Borrower, StudentDetails

logger = logging.getLogger(__name__)


class AddNewBook(graphene.Mutation):
    ok = graphene.Boolean()
    message = graphene.String()

    class Arguments:
        def __init__(self):
            pass

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
            return {"ok": True, "message": "Book added successfully"}

        except Category.DoesNotExist:
            return {"ok": False, "message": "Category is not present"}

        except kwargs.get("publisher") is None:
            return {"ok": False, "message": "Publisher is not present"}

        except kwargs.get("isbn") is None:
            return {"ok": False, "message": "ISBN is not present"}

        except kwargs.get("title") is None:
            return {"ok": False, "message": "Title is not present"}

        except Exception as e:
            logger.error(e)
            return {"ok": False, "message": "Book already present."}


class AddNewCategory(graphene.Mutation):
    ok = graphene.Boolean()
    message = graphene.String()

    class Arguments:
        def __init__(self):
            pass

        category_name = graphene.String(required=True)

    @staticmethod
    def mutate(self, info, **kwargs):
        try:
            new_category = Category(category_name=kwargs.get("category_name"))
            new_category.save()
            return {"ok": True, "message": "Category created successfully"}
        except Exception as e:
            logger.error(e)
            return {"ok": False, "message": "Category already present"}


class AddNewDepartment(graphene.Mutation):
    ok = graphene.Boolean()
    message = graphene.String()

    class Arguments:
        def __init__(self):
            pass

        department_name = graphene.String(required=True)

    @staticmethod
    def mutate(self, info, **kwargs):
        try:
            new_department = Department(department_name=kwargs.get("department_name"))
            new_department.save()
            return {"ok": True, "message": "Department created successfully"}
        except Exception as e:
            logger.error(e)
            return {"ok": False, "message": "Department already exist"}


class BorrowBooksByStudent(graphene.Mutation):
    ok = graphene.Boolean()
    message = graphene.String()

    class Arguments:
        def __init__(self):
            pass

        book_ids = graphene.List(graphene.ID)
        student_id = graphene.ID(required=True)

    @staticmethod
    def mutate(self, info, student_id, book_ids, **kwargs):
        try:
            student = StudentDetails.objects.get(student_id=student_id)
            for id in book_ids:
                book = BookDetails.objects.get(id=id)
                book.no_of_copies_current = book.no_of_copies_current - 1
                book.save()
                borrower = Borrower.objects.create()
                borrower.borrowed_from_date = datetime.date.today()
                borrower.borrowed_to_date = datetime.date.today() + datetime.timedelta(days=7)
                borrower.book = book
                borrower.save()
                student.borrower.add(borrower)
                student.save()

            return {"ok": True, "message": "Borrowed Books added successfully to student " + student.student_name}

        except Exception as e:
            logger.error(e)
            return {"ok": False, "message": "Something went wrong"}


class Mutation(graphene.ObjectType):
    add_new_category = AddNewCategory.Field()
    add_new_book = AddNewBook.Field()
    add_new_department = AddNewDepartment.Field()
    borrow_book_by_student = BorrowBooksByStudent.Field()
