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


class ExampleForm(forms.Form):
    """
    A simple example form to demonstrate CSRF token inclusion
    and safe handling of user input.
    """
    name = forms.CharField(max_length=100, label="Your Name")
    email = forms.EmailField(label="Email Address")
    message = forms.CharField(
        widget=forms.Textarea,
        label="Message",
        help_text="Enter your message here."
    )

    def clean_name(self):
        name = self.cleaned_data["name"]
        # Example of input sanitization — stripping unwanted spaces
        return name.strip()
