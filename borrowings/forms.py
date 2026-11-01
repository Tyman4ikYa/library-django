from django import forms
from django.utils import timezone
from .models import Borrowing
from library.models import Book

class BorrowingForm(forms.ModelForm):
    books = forms.ModelMultipleChoiceField(
        queryset=Book.objects.filter(available=True),
        widget=forms.CheckboxSelectMultiple,
        label="Выберите книги",
        required=True
    )

    class Meta:
        model = Borrowing
        fields = ["books", "due_date", "comment"]
        widgets = {
            "due_date": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "comment": forms.Textarea(attrs={"class": "form-control", "rows": 3, "placeholder": "Комментарий"}),
        }
        labels = {
            "due_date": "Дата возврата",
            "comment": "Комментарий",
        }

    def clean_due_date(self):
        due_date = self.cleaned_data["due_date"]
        if due_date < timezone.now().date():
            raise forms.ValidationError("Дата возврата не может быть в прошлом.")
        return due_date