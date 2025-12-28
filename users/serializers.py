from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer, UserSerializer
from rest_framework import serializers
from users.models import Author
from books.models import Book

class UserCreateSerializer(BaseUserCreateSerializer):
    class Meta(BaseUserCreateSerializer.Meta):
        fields = ['id', 'email', 'password', 'first_name', 'last_name', 'address', 'phone_number']


class UserViewSerializer(UserSerializer):
    class Meta(UserSerializer.Meta):
        fields = ['id', 'first_name', 'last_name', 'email', 'address', 'phone_number']


        
class SimpleBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'title', 'isbn', 'category']

class AuthorViewSerializer(serializers.ModelSerializer):
    books = SimpleBookSerializer(many=True, read_only=True)
    class Meta:
        model = Author
        fields = ['id', 'name', 'books', 'biography']