from rest_framework import serializers
from .models import Genre, Author, Book

class GenreSerializer(serializers.ModelSerializer):
    books_count = serializers.SerializerMethodField()

    class Meta:
        model = Genre
        fields = ['id', 'name', 'slug', 'books_count']
        read_only_fields = ['id']

    def get_books_count(self, obj):
        return obj.books.count()

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['id', 'first_name', 'last_name', 'birth_date']
        read_only_fields = ['id']

class BookSerializer(serializers.ModelSerializer):
    author_name = serializers.SerializerMethodField()
    genres_names = serializers.SerializerMethodField()

    class Meta:
        model = Book
        fields = [
            'id', 'title', 'slug', 'description', 'price', 'year', 
            'isbn', 'available', 'created_at', 'author', 
            'author_name', 'genres', 'genres_names'
        ]
        read_only_fields = ['id', 'created_at', 'slug']

    def get_author_name(self, obj):
        return f"{obj.author.last_name} {obj.author.first_name}"

    def get_genres_names(self, obj):
        return [genre.name for genre in obj.genres.all()]