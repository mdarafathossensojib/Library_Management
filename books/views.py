from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.filters import SearchFilter
from books.models import Book, BorrowRecord, Record
from books.serializers import BookSerializer, RecordSerializer, BorrowCreateSerializer, BorrowListSerializer
from books.pagination import DefaultPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, DestroyModelMixin, ListModelMixin
from books.permissions import IsAdminOrReadOnly
from datetime import timezone

# Create your views here.

class BookViewSet(ModelViewSet):
    permission_classes = [IsAdminOrReadOnly]
    queryset = Book.objects.select_related('author').all()
    serializer_class = BookSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    pagination_class = DefaultPagination
    search_fields = ['title', 'category']

    
class RecordViewSet(CreateModelMixin, RetrieveModelMixin, DestroyModelMixin, ListModelMixin, GenericViewSet):
    serializer_class = RecordSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Record.objects.none()
        
        return Record.objects.prefetch_related('borrow_records__book').filter(member=self.request.user)
    
    def list(self, request, *args, **kwargs):
        record, created = Record.objects.get_or_create(member=request.user)
        serializer = self.get_serializer(record)
        return Response([serializer.data])
    
class RecordBookViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return BorrowRecord.objects.none()
        
        return BorrowRecord.objects.select_related('book').filter(
            record__member=self.request.user
        )

    def get_serializer_class(self):
        if self.action == 'create':
            return BorrowCreateSerializer
        return BorrowListSerializer

    def get_serializer_context(self):
        if getattr(self, 'swagger_fake_view', False):
            return Record.objects.none()
        
        context = super().get_serializer_context()
        context['record'] = Record.objects.get(member=self.request.user)
        return context
    
    @action(detail=True, methods=['post'])
    def return_book(self, request, pk=None):
        borrow = self.get_object()

        if borrow.is_returned:
            return Response(
                {'error': 'Already returned'},
                status=status.HTTP_400_BAD_REQUEST
            )

        borrow.is_returned = True
        borrow.return_date = timezone.now().date()
        borrow.save()

        book = borrow.book
        book.is_available = True
        book.save()

        return Response({'status': 'Book returned successfully'})