from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Book

class BookAPITest(APITestCase):

    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username="testuser", password="password123")
        
        # Create a sample book
        self.book = Book.objects.create(
            title="Test Book",
            author="Author Name",
            publication_year=2024
        )
    
    def test_book_list_authenticated(self):
        # Login before making request
        self.client.login(username="testuser", password="password123")

        response = self.client.get("/api/books/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("title", response.data[0])  # ✅ ensures data is returned

    def test_book_list_unauthenticated(self):
        response = self.client.get("/api/books/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)  # or 401 depending on settings


def test_filter_books_by_author(self):
    url = f"{self.url}?author=Kent Beck"
    response = self.client.get(url)
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertEqual(len(response.data), 1)
    self.assertEqual(response.data[0]["author"], "Kent Beck")
