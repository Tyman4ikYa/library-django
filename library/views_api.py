from rest_framework import viewsets
from .models import Genre, Author, Book
from .serializers import GenreSerializer, AuthorSerializer, BookSerializer

class GenreViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    lookup_field = 'slug'

class AuthorViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    lookup_field = 'pk'

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.filter(available=True).select_related('author').prefetch_related('genres')
    serializer_class = BookSerializer
    lookup_field = 'slug'