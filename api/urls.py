from django.urls import path, include
from api import views
from books.views import BookViewSet, RecordBookViewSet, RecordViewSet
from users.views import AuthorViewSet
from rest_framework_nested import routers

router = routers.DefaultRouter()
router.register('books', BookViewSet, basename='books')
router.register('record', RecordViewSet, basename='record')
router.register('author', AuthorViewSet, basename='author')

record_router = routers.NestedDefaultRouter(router, 'record', lookup='record')
record_router.register('borrow-books', RecordBookViewSet, basename='borrow-books')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(record_router.urls)),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),

]
