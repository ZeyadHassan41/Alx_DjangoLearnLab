import os
import django

# Ensure Django knows where the settings are
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "LibraryProject.settings")
django.setup()

from relationship_app.models import Author, Book, Library, Librarian

# 1. Query all books by a specific author
author_name = "Ahmed Khaled Tawfik"
try:
    author = Author.objects.get(name=author_name)

    # Using .filter() instead of reverse relation
    books_by_author = Book.objects.filter(author=author)

    print(f"Books by {author.name}:")
    for book in books_by_author:
        print(f"- {book.title}")

except Author.DoesNotExist:
    print(f"Author '{author_name}' not found.")

# 2. List all books in a library
library_name = "Central Library"
try:
    library = Library.objects.get(name=library_name)
    books_in_library = library.books.all()
    print(f"\nBooks in {library.name}:")
    for book in books_in_library:
        print(f"- {book.title}")
except Library.DoesNotExist:
    print(f"Library '{library_name}' not found.")

# 3. Retrieve the librarian for a library
try:
    librarian = library.librarian
    print(f"\nLibrarian of {library.name}: {librarian.name}")
except Librarian.DoesNotExist:
    print(f"Librarian for {library.name} not found.")
