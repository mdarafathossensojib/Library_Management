from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter
from books.models import Book, BorrowRecord
from books.serializers import BookSerializer
from books.pagination import DefaultPagination
from django_filters.rest_framework import DjangoFilterBackend

# Create your views here.

class BookViewSet(ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    pagination_class = DefaultPagination
    search_fields = ['title', 'category']

    
