from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter
from users.models import Author
from users.serializers import AuthorViewSerializer
from books.pagination import DefaultPagination
from django_filters.rest_framework import DjangoFilterBackend
from books.permissions import IsAdminOrReadOnly

# Create your views here.

class AuthorViewSet(ModelViewSet):
    permission_classes = [IsAdminOrReadOnly]
    queryset = Author.objects.prefetch_related('books').all()
    serializer_class = AuthorViewSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    pagination_class = DefaultPagination
    search_fields = ['name']