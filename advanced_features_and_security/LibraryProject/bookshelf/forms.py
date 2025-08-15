# bookshelf/forms.py
from django import forms
from .models import Book

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ["title", "author", "publication_year"]

    def clean_publication_year(self):
        year = self.cleaned_data["publication_year"]
        if year < 0 or year > 3000:
            raise forms.ValidationError("Invalid publication year.")
        return year


class BookSearchForm(forms.Form):
    q = forms.CharField(
        label="Search",
        max_length=200,
        required=False,
        help_text="Search by title or author."
    )
