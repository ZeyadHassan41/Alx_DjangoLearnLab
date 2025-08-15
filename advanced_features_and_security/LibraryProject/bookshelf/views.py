from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import permission_required
from .models import Book
from .forms import ExampleForm  # ✅ Added import


@permission_required('bookshelf.can_view', raise_exception=True)
def book_list(request):
    """List all books - requires can_view permission."""
    books = Book.objects.all()
    return render(request, 'bookshelf/book_list.html', {'books': books})


@permission_required('bookshelf.can_create', raise_exception=True)
def book_create(request):
    """Create a new book - requires can_create permission."""
    if request.method == 'POST':
        title = request.POST.get('title')
        author = request.POST.get('author')
        publication_year = request.POST.get('publication_year')
        if title and author and publication_year:
            Book.objects.create(
                title=title,
                author=author,
                publication_year=publication_year
            )
            return redirect('book_list')
    return render(request, 'bookshelf/book_form.html')


@permission_required('bookshelf.can_edit', raise_exception=True)
def book_edit(request, pk):
    """Edit an existing book - requires can_edit permission."""
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        book.title = request.POST.get('title')
        book.author = request.POST.get('author')
        book.publication_year = request.POST.get('publication_year')
        book.save()
        return redirect('book_list')
    return render(request, 'bookshelf/book_form.html', {'book': book})


@permission_required('bookshelf.can_delete', raise_exception=True)
def book_delete(request, pk):
    """Delete a book - requires can_delete permission."""
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        book.delete()
        return redirect('book_list')
    return render(request, 'bookshelf/book_confirm_delete.html', {'book': book})


def example_form_view(request):
    """
    Example form view to demonstrate CSRF protection and safe form handling.
    """
    if request.method == 'POST':
        form = ExampleForm(request.POST)
        if form.is_valid():
            # Safely handle validated and sanitized input
            cleaned_data = form.cleaned_data
            return render(request, 'bookshelf/form_success.html', {
                'name': cleaned_data['name'],
                'email': cleaned_data['email'],
                'message': cleaned_data['message']
            })
    else:
        form = ExampleForm()
    return render(request, 'bookshelf/form_example.html', {'form': form})
