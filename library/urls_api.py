from rest_framework.routers import DefaultRouter
from .views_api import GenreViewSet, AuthorViewSet, BookViewSet

router = DefaultRouter()
router.register('genres', GenreViewSet, basename='genre')
router.register('authors', AuthorViewSet, basename='author')
router.register('books', BookViewSet, basename='book')

urlpatterns = router.urls