from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.utils import timezone

from library.models import Book
from .forms import BorrowingForm
from .models import Borrowing
from .services import create_borrowing


@login_required
def borrowing_create_view(request):
    available_books = Book.objects.filter(available=True).select_related("author")

    if request.method == "POST":
        form = BorrowingForm(request.POST)
        if form.is_valid():
            book_ids = request.POST.getlist("book_ids")
            if not book_ids:
                messages.error(request, "Выберите хотя бы одну книгу.")
                return render(request, "borrowings/borrowing_form.html", {
                    "form": form, "books": available_books,
                })

            books = [{"book": get_object_or_404(Book, id=bid), "quantity": 1} for bid in book_ids]
            borrowing = create_borrowing(
                reader=request.user,
                books=books,
                due_date=form.cleaned_data["due_date"],
                comment=form.cleaned_data.get("comment", ""),
            )
            messages.success(request, f"Выдача №{borrowing.pk} создана!")
            return redirect("borrowings:detail", pk=borrowing.pk)
    else:
        form = BorrowingForm()

    return render(request, "borrowings/borrowing_form.html", {
        "form": form, "books": available_books,
    })


@login_required
def borrowing_detail_view(request, pk):
    borrowing = get_object_or_404(
        Borrowing.objects.select_related("reader").prefetch_related("items__book"),
        pk=pk,
        reader=request.user,
    )
    return render(request, "borrowings/borrowing_detail.html", {"borrowing": borrowing})


@login_required
def borrowing_list_view(request):
    borrowings = Borrowing.objects.filter(reader=request.user).prefetch_related("items")
    return render(request, "borrowings/borrowing_list.html", {"borrowings": borrowings})


@login_required
@require_POST
def borrowing_return_view(request, pk):
    borrowing = get_object_or_404(Borrowing, pk=pk, reader=request.user)

    if not borrowing.can_be_returned():
        messages.error(request, "Эту выдачу уже нельзя вернуть.")
        return redirect("borrowings:detail", pk=borrowing.pk)

    borrowing.status = Borrowing.STATUS_RETURNED
    borrowing.returned_at = timezone.now()
    borrowing.save(update_fields=["status", "returned_at"])

    messages.success(request, f"Выдача №{borrowing.pk} возвращена.")
    return redirect("borrowings:detail", pk=borrowing.pk)