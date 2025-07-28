from django.shortcuts import render
from .models import Book

# Function-based View: List all books
def list_books(request):
    books = Book.objects.all()  # ✅ Required exact call
    return render(request, 'relationship_app/list_books.html', {'books': books})  # ✅ Required exact template path
