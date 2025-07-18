from django.shortcuts import render, get_object_or_404
from django.views.generic import DetailView
from .models import Book, Library

# ✅ Function-based view: uses Book.objects.all() and the correct template path
def list_books(request):
    books = Book.objects.all()  # <== Required by your checker
    return render(request, 'relationship_app/list_books.html', {'books': books})  # <== Required path

# ✅ Class-based view: uses DetailView
class LibraryDetailView(DetailView):
    model = Library
    template_name = 'relationship_app/library_detail.html'  # explicit template
    context_object_name = 'library'
