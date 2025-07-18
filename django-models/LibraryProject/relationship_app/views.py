from django.shortcuts import render, get_object_or_404
from django.views.generic import DetailView
from .models import Book, Library

# ✅ Function-based view that uses Book.objects.all()
def list_books(request):
    books = Book.objects.all()  # <-- This now meets the requirement
    return render(request, 'relationship_app/list_books.html', {'books': books})

# ✅ Class-based view for a specific Library
class LibraryDetailView(DetailView):
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'
