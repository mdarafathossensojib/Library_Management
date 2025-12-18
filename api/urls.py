from django.urls import path, include
from api import views
from books.views import BookViewSet
from rest_framework_nested import routers

router = routers.DefaultRouter()
router.register('books', BookViewSet, basename='books')

urlpatterns = [
    path('', include(router.urls)),
]
