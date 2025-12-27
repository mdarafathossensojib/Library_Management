from django.contrib import admin
from books.models import Book, BorrowRecord, Record

# Register your models here.

admin.site.register(Book)
admin.site.register(BorrowRecord)
admin.site.register(Record)