from rest_framework import serializers
from books.models import Book, BorrowRecord, Record
from users.models import Author
from django.utils import timezone

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['id', 'name']
        
class BookSerializer(serializers.ModelSerializer):
    author = AuthorSerializer()

    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'isbn', 'category', 'is_available']

class BookCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'isbn', 'category', 'is_available']

class BookUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['title', 'category', 'is_available']

class BorrowCreateSerializer(serializers.Serializer):
    book_name = serializers.PrimaryKeyRelatedField(
        queryset=Book.objects.filter(is_available=True),
        source='book'
    )
    return_date = serializers.DateField()

    def create(self, validated_data):
        record = self.context['record']
        book = validated_data['book']
        return_date = validated_data['return_date']
        
        borrow = BorrowRecord.objects.create(
            book=book,
            record=record,
            return_date=return_date
        )

        book.is_available = False
        book.save()
        return borrow

class BorrowReturnSerializer(serializers.ModelSerializer):
    class Meta:
        model = BorrowRecord
        fields = ['is_returned']

    def update(self, instance, validated_data):
        if validated_data.get('is_returned') and not instance.is_returned:
            instance.is_returned = True
            instance.return_date = timezone.now().date()
            instance.save()

            instance.book.is_available = True
            instance.book.save()

        return instance

class BorrowListSerializer(serializers.ModelSerializer):
    book = BookSerializer(read_only=True)

    class Meta:
        model = BorrowRecord
        fields = ['id', 'book', 'borrow_date', 'return_date', 'is_returned']


class RecordSerializer(serializers.ModelSerializer):
    borrow_records = BorrowListSerializer(many=True, read_only=True)

    class Meta:
        model = Record
        fields = ['id', 'member', 'borrow_records']
        read_only_fields = ['member']

    