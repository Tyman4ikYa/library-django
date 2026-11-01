from django.shortcuts import render, get_object_or_404
from .models import Book, Reader

def book_list(request):
    books = Book.objects.all()
    return render(request, 'library/book_list.html', {'books': books})

def book_detail(request, slug):
    book = get_object_or_404(Book, slug=slug)
    return render(request, 'library/book_detail.html', {'book': book})

def reader_list(request):
    readers = Reader.objects.all()
    return render(request, 'library/reader_list.html', {'readers': readers})

def reader_detail(request, pk):
    reader = get_object_or_404(Reader, pk=pk)
    return render(request, 'library/reader_detail.html', {'reader': reader})