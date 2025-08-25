from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from .models import Book


class BookAPITests(APITestCase):
    def setUp(self):
        self.book = Book.objects.create(
            title="Test Driven Development",
            author="Kent Beck",
            publication_year=2003
        )
        self.url = reverse("book-list")  # Assuming DRF router registered as book-list

    def test_get_books_list(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("title", response.data[0])  # <-- checks payload
        self.assertEqual(response.data[0]["title"], "Test Driven Development")

    def test_create_book(self):
        data = {
            "title": "Clean Code",
            "author": "Robert C. Martin",
            "publication_year": 2008
        }
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["title"], "Clean Code")

def test_filter_books_by_author(self):
    url = f"{self.url}?author=Kent Beck"
    response = self.client.get(url)
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertEqual(len(response.data), 1)
    self.assertEqual(response.data[0]["author"], "Kent Beck")
