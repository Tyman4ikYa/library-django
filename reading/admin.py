from django.contrib import admin
from .models import ReadingList, ReadingListItem


class ReadingListItemInline(admin.TabularInline):
    model = ReadingListItem
    extra = 0
    fields = ("book", "quantity", "added_at")
    readonly_fields = ("added_at",)


@admin.register(ReadingList)
class ReadingListAdmin(admin.ModelAdmin):
    list_display = ("user", "item_count_display", "updated_at")
    search_fields = ("user__username", "user__email")
    list_select_related = ("user",)
    inlines = (ReadingListItemInline,)

    @admin.display(description="Позиций")
    def item_count_display(self, obj):
        return obj.item_count


@admin.register(ReadingListItem)
class ReadingListItemAdmin(admin.ModelAdmin):
    list_display = ("reading_list", "book", "quantity", "added_at")
    list_filter = ("added_at",)
    search_fields = ("book__title", "reading_list__user__username")
    list_select_related = ("reading_list", "book")