from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from library.models import Book


class Borrowing(models.Model):
    STATUS_ACTIVE = "active"
    STATUS_RETURNED = "returned"
    STATUS_OVERDUE = "overdue"

    STATUS_CHOICES = [
        (STATUS_ACTIVE, "Активна"),
        (STATUS_RETURNED, "Возвращена"),
        (STATUS_OVERDUE, "Просрочена"),
    ]

    reader = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name="borrowings",
        verbose_name="Читатель",
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_ACTIVE,
        verbose_name="Статус",
    )
    due_date = models.DateField(verbose_name="Дата возврата")
    returned_at = models.DateTimeField(
        null=True, blank=True, verbose_name="Дата фактического возврата"
    )
    comment = models.TextField(blank=True, verbose_name="Комментарий")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата выдачи")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    class Meta:
        verbose_name = "Выдача"
        verbose_name_plural = "Выдачи"
        ordering = ["-created_at"]

    def __str__(self):
        return f"Выдача №{self.pk} — {self.reader.username}"

    def can_be_returned(self):
        return self.status in (self.STATUS_ACTIVE, self.STATUS_OVERDUE)

    def is_overdue(self):
        return self.status == self.STATUS_ACTIVE and self.due_date < timezone.now().date()


class BorrowingItem(models.Model):
    borrowing = models.ForeignKey(
        Borrowing,
        on_delete=models.CASCADE,
        related_name="items",
        verbose_name="Выдача",
    )
    book = models.ForeignKey(
        Book,
        on_delete=models.PROTECT,
        verbose_name="Книга",
    )
    book_title = models.CharField(max_length=200, verbose_name="Название (снапшот)")
    book_author = models.CharField(max_length=200, verbose_name="Автор (снапшот)")
    quantity = models.PositiveIntegerField(default=1, verbose_name="Количество")
    added_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата добавления")

    class Meta:
        verbose_name = "Позиция выдачи"
        verbose_name_plural = "Позиции выдачи"

    def __str__(self):
        return f"{self.book_title} × {self.quantity}"