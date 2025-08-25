from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import generics, filters
from django_filters import rest_framework as filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Book
from .serializers import BookSerializer


# List all books (anyone can access) with filtering, searching, and ordering
class BookListView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [AllowAny]  # Public access

    # Enable filtering, searching, and ordering
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]

    # Filtering options: allows filtering by title, publication_year, and author
    filterset_fields = ['title', 'publication_year', 'author']

    # Search options: users can search by title and author's name
    search_fields = ['title', 'author__name']

    # Ordering options: users can order results by title or publication_year
    ordering_fields = ['title', 'publication_year']
    ordering = ['title']  # Default ordering


# Retrieve a single book by ID (anyone can access)
class BookDetailView(generics.RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [AllowAny]  # Public access


# Create a new book (authenticated users only)
class BookCreateView(generics.CreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

    # Optional customization: attach current user’s ID if needed
    def perform_create(self, serializer):
        serializer.save()


# Update an existing book (authenticated users only)
class BookUpdateView(generics.UpdateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):
        serializer.save()


# Delete a book (authenticated users only)
class BookDeleteView(generics.DestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

class BookFilter(filters.FilterSet):
    class Meta:
        model = Book
        fields = ['title', 'author', 'publication_year']


class BookListView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = BookFilter