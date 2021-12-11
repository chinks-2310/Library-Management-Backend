from django.contrib import admin

from .models import Category, BookDetails, Borrower, Department, StudentDetails


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "category_name")
    search_fields = ("category_name",)


@admin.register(BookDetails)
class BookDetailsAdmin(admin.ModelAdmin):
    list_display = (
        "id", "isbn", "title", "publication_year", "language", "no_of_actual_copies", "no_of_copies_current",
        "publisher",
        "category")
    search_fields = ("title", "publication_year", "language", "publisher", "category")
    list_filter = ("publication_year", "publisher", "language", "category")


@admin.register(Borrower)
class BorrowerAdmin(admin.ModelAdmin):
    list_display = ("id", "borrowed_from_date", "borrowed_to_date", "actual_return_date", "is_return")
    search_fields = ("id", "actual_return_date")
    list_filter = ("borrowed_from_date", "borrowed_to_date", "actual_return_date")


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ("id", "department_name")
    search_fields = ("id", "department_name")


@admin.register(StudentDetails)
class StudentDetailsAdmin(admin.ModelAdmin):
    list_display = ("student_id", "student_name", "gender", "date_of_birth", "department", "contact_number")
    search_fields = ("student_name", "department")
    list_filter = ("department", "gender")
