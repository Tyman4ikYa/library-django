from django.contrib import admin
from django.db.models import Count
from .models import Author, Genre, Book


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "birth_date")
    search_fields = ("first_name", "last_name")
    list_filter = ("birth_date",)
    ordering = ("last_name",)


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "books_count")
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}
    verbose_name = "Жанр"
    verbose_name_plural = "Жанры"

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.annotate(books_count=Count("books"))

    @admin.display(description="Книг в жанре")
    def books_count(self, obj):
        return obj.books_count


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "year", "price", "available")
    list_filter = ("available", "author", "genres")
    search_fields = ("title",)
    list_editable = ("price", "available")
    prepopulated_fields = {"slug": ("title",)}
    readonly_fields = ("created_at", "updated_at")
    list_select_related = ("author",)
    date_hierarchy = "created_at"

    fieldsets = (
        ("Основное", {
            "fields": ("title", "slug", "year")
        }),
        ("Автор и жанры", {
            "fields": ("author", "genres")
        }),
        ("Издание", {
            "fields": ("price", "available")
        }),
        ("Служебное", {
            "fields": ("created_at", "updated_at"),
            "classes": ("collapse",),
        }),
    )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related("author").prefetch_related("genres")