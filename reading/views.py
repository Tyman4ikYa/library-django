from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from library.models import Book
from .models import ReadingList, ReadingListItem


@login_required
def add_to_reading_view(request, book_id):
    if request.method != "POST":
        return redirect("/")

    book = get_object_or_404(Book, id=book_id)
    reading_list, _ = ReadingList.objects.get_or_create(user=request.user)

    item, created = ReadingListItem.objects.get_or_create(
        reading_list=reading_list,
        book=book,
        defaults={"quantity": 1},
    )

    if created:
        messages.success(request, f"«{book.title}» добавлена в список чтения.")
    else:
        item.quantity += 1
        item.save()
        messages.success(request, f"«{book.title}» — теперь {item.quantity} шт.")

    return redirect(request.META.get("HTTP_REFERER", "/"))


@login_required
def reading_list_detail_view(request):
    reading_list, _ = ReadingList.objects.get_or_create(user=request.user)
    items = reading_list.items.select_related("book", "book__author").all()

    context = {
        "reading_list": reading_list,
        "items": items,
    }
    return render(request, "reading/reading_list.html", context)


@login_required
def update_reading_item_view(request, item_id):
    if request.method != "POST":
        return redirect("reading:detail")

    item = get_object_or_404(
        ReadingListItem, id=item_id, reading_list__user=request.user
    )

    try:
        quantity = int(request.POST.get("quantity", 1))
    except (TypeError, ValueError):
        messages.error(request, "Некорректное количество.")
        return redirect("reading:detail")

    if quantity < 1:
        item.delete()
        messages.info(request, "Позиция удалена из списка.")
    else:
        item.quantity = min(quantity, 99)
        item.save()
        messages.success(request, "Количество обновлено.")

    return redirect("reading:detail")


@login_required
def remove_reading_item_view(request, item_id):
    if request.method != "POST":
        return redirect("reading:detail")

    item = get_object_or_404(
        ReadingListItem, id=item_id, reading_list__user=request.user
    )
    book_title = item.book.title
    item.delete()
    messages.info(request, f"«{book_title}» удалена из списка.")

    return redirect("reading:detail")