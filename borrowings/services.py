from django.db import transaction

from .models import Borrowing, BorrowingItem


@transaction.atomic
def create_borrowing(reader, books, due_date, comment=""):
    """
    Создаёт выдачу.
    books — список словарей [{"book": Book, "quantity": 1}, ...]
    """
    borrowing = Borrowing.objects.create(
        reader=reader,
        due_date=due_date,
        comment=comment,
        status=Borrowing.STATUS_ACTIVE,
    )

    for item in books:
        book = item["book"]
        BorrowingItem.objects.create(
            borrowing=borrowing,
            book=book,
            book_title=book.title,
            book_author=f"{book.author}",
            quantity=item.get("quantity", 1),
        )

    return borrowing