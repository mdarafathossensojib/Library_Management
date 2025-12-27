from rest_framework import serializers
from books.models import Book, BorrowRecord, Record
from users.models import Author


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['id', 'name']
        
class BookSerializer(serializers.ModelSerializer):
    author = AuthorSerializer()

    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'isbn', 'category', 'is_available']


class BorrowCreateSerializer(serializers.Serializer):
    book_name = serializers.PrimaryKeyRelatedField(
        queryset=Book.objects.filter(is_available=True),
        source='book'
    )

    def create(self, validated_data):
        record = self.context['record']
        book = validated_data['book']

        borrow = BorrowRecord.objects.create(
            book=book,
            record=record
        )

        book.is_available = False
        book.save()
        return borrow

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

    