from django.db import models
from django.utils import timezone
from users.models import Author, Member
from uuid import uuid4

# Create your models here.

class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey(
        Author,
        on_delete=models.CASCADE,
        related_name="books"
    )
    isbn = models.CharField(max_length=13, unique=True)
    category = models.CharField(max_length=100)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Record(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    member = models.OneToOneField(Member, on_delete=models.CASCADE, related_name='record')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Record of {self.member.first_name}"
    
class BorrowRecord(models.Model):
    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        related_name="borrow_book"
    )
    record = models.ForeignKey(
        Record,
        on_delete=models.CASCADE,
        related_name="borrow_records"
    )
    borrow_date = models.DateField(default=timezone.now)
    return_date = models.DateField(null=True, blank=True)
    is_returned = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.book.title} - {self.record.member.first_name}"
        
