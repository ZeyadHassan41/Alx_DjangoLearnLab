from rest_framework import serializers
from .models import Author, Book
from datetime import datetime


# BookSerializer: Serializes book data and validates publication year
class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'title', 'publication_year', 'author']

    # Custom validation: publication_year cannot be in the future
    def validate_publication_year(self, value):
        current_year = datetime.now().year
        if value > current_year:
            raise serializers.ValidationError("Publication year cannot be in the future.")
        return value


# AuthorSerializer: Serializes author data and includes nested book details
class AuthorSerializer(serializers.ModelSerializer):
    # Nested representation of books
    books = BookSerializer(many=True, read_only=True)

    class Meta:
        model = Author
        fields = ['id', 'name', 'books']
