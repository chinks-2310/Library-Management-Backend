from ..models import BookDetails, StudentDetails, Borrower


class BookViewResolver:
    def __init__(self):
        pass

    def __call__(self, source, info, **kwargs):
        book_details = BookDetails.objects.all()
        return book_details


class StudentViewResolver:
    def __init__(self):
        pass

    def __call__(self, source, info, **kwargs):
        result = []
        students = StudentDetails.objects.all()
        student_details = {}
        borrower = {}
        books = []
        for student in students:
            b = BookDetails.objects.get(id=student.borrower.id)
            print(b)
            student_details["student_name"] = student.student_name
            student_details["gender"] = student.gender
            student_details["date_of_birth"] = student.date_of_birth
            borrower["borrowed_from_date"] = student.borrower.borrowed_from_date
            borrower["borrowed_to_date"] = student.borrower.borrowed_to_date
            books.append(b)
            student_details["borrower"] = borrower
            student_details["borrower"]["books"] = books
            result.append(student_details)
        return result
