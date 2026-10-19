from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from library.models import Book


class ReadingList(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="reading_list",
        verbose_name="Пользователь",
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    class Meta:
        verbose_name = "Список чтения"
        verbose_name_plural = "Списки чтения"

    def __str__(self):
        return f"Список чтения {self.user.username}"

    @property
    def total_books(self):
        return self.items.count()

    @property
    def item_count(self):
        return sum(item.quantity for item in self.items.all())


class ReadingListItem(models.Model):
    reading_list = models.ForeignKey(
        ReadingList,
        on_delete=models.CASCADE,
        related_name="items",
        verbose_name="Список",
    )
    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        related_name="in_reading_lists",
        verbose_name="Книга",
    )
    quantity = models.PositiveIntegerField(default=1, verbose_name="Количество")
    added_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата добавления")

    class Meta:
        verbose_name = "Позиция списка"
        verbose_name_plural = "Позиции списка"
        unique_together = ("reading_list", "book")
        ordering = ("-added_at",)

    def __str__(self):
        return f"{self.book.title} ({self.quantity} шт.)"

    @property
    def subtotal(self):
        return self.book.price * self.quantity