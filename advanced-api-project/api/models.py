from django.db import models

# Author model: Represents a writer who may have multiple books
class Author(models.Model):
    name = models.CharField(max_length=255)  # Storing author’s name

    def __str__(self):
        return self.name


# Book model: Represents a book written by an Author
class Book(models.Model):
    title = models.CharField(max_length=255)  # Title of the book
    publication_year = models.IntegerField()  # Year the book was published
    author = models.ForeignKey(
        Author,
        related_name="books",  # Helps in reverse lookup (author.books.all())
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.title} ({self.publication_year})"
