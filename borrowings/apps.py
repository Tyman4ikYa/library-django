from django.apps import AppConfig


class BorrowingsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "borrowings"
    verbose_name = "Выдачи"

    def ready(self):
        import borrowings.signals  # noqa