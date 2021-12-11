import datetime

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


def current_year():
    return datetime.date.today().year


def max_value_current_year(value):
    return MaxValueValidator(current_year())(value)


GENDER_CHOICES = (
    (1, 'Male'),
    (2, 'Female'),
)


class Category(models.Model):
    category_name = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name_plural = "Category"

    def __str__(self):
        return u'{0}'.format(self.category_name)


class BookDetails(models.Model):
    isbn = models.CharField(max_length=20, unique=True)
    title = models.CharField(max_length=100)
    publication_year = models.PositiveIntegerField(default=current_year(),
                                                   validators=[MinValueValidator(1984), max_value_current_year])
    language = models.CharField(max_length=100)
    no_of_actual_copies = models.PositiveIntegerField(default=0)
    no_of_copies_current = models.PositiveIntegerField(default=0)
    publisher = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name_plural = "Book Details"

    def __str__(self):
        return u'{0}'.format(self.title)


class Department(models.Model):
    department_name = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = "Department"

    def __str__(self):
        return u'{0}'.format(self.department_name)


class Borrower(models.Model):
    borrowed_from_date = models.DateField(null=True, blank=False)
    borrowed_to_date = models.DateField(null=True, blank=False)
    actual_return_date = models.DateField(null=True, blank=True)
    is_return = models.BooleanField(default=False)
    books = models.ManyToManyField(BookDetails)

    class Meta:
        verbose_name_plural = "Borrower"

    # def __str__(self):
    #     return u'{0}'.format(self.id)


class StudentDetails(models.Model):
    student_id = models.AutoField(primary_key=True)
    student_name = models.CharField(max_length=100)
    gender = models.IntegerField(choices=GENDER_CHOICES)
    date_of_birth = models.DateField(null=True, blank=True)
    borrower = models.ManyToManyField(Borrower)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)
    contact_number = models.CharField(max_length=12, unique=True)

    class Meta:
        verbose_name_plural = "Students"
