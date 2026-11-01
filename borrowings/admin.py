from django.contrib import admin
from .models import Borrowing, BorrowingItem

class BorrowingItemInline(admin.TabularInline):
    model = BorrowingItem
    extra = 0
    readonly_fields = ('book', 'book_title', 'book_author', 'quantity')
    can_delete = False

@admin.register(Borrowing)
class BorrowingAdmin(admin.ModelAdmin):
    list_display = ('id', 'reader', 'status', 'due_date', 'created_at')
    list_filter = ('status', 'created_at', 'due_date')
    search_fields = ('reader__username', 'reader__email')
    list_editable = ('status',)
    date_hierarchy = 'created_at'
    inlines = [BorrowingItemInline]

@admin.register(BorrowingItem)
class BorrowingItemAdmin(admin.ModelAdmin):
    list_display = ('borrowing', 'book_title', 'book_author', 'quantity')
    search_fields = ('book_title', 'book_author', 'borrowing__reader__username')