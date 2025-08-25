from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status

from .models import Author, Book


class BookAPITests(TestCase):
    """
    Test suite for Book API endpoints:
    - CRUD: list, retrieve, create, update, delete
    - Filtering: title, author, publication_year
    - Searching: title, author name
    - Ordering: title, publication_year
    - Permissions: unauthenticated read-only; write ops require authentication
    """

    @classmethod
    def setUpTestData(cls):
        # Users
        User = get_user_model()
        cls.user = User.objects.create_user(
            username="tester", email="tester@example.com", password="strong-pass-123"
        )

        # Authors
        cls.author1 = Author.objects.create(name="George Orwell")
        cls.author2 = Author.objects.create(name="Ibrahim Al-Sakran")

        # Books
        cls.book1 = Book.objects.create(
            title="1984", publication_year=1949, author=cls.author1
        )
        cls.book2 = Book.objects.create(
            title="Animal Farm", publication_year=1945, author=cls.author1
        )
        cls.book3 = Book.objects.create(
            title="رقائق القرآن", publication_year=2010, author=cls.author2
        )

    def setUp(self):
        self.client = APIClient()

    # -------- Helpers

    def _auth(self):
        """Force-authenticate requests as a valid user."""
        self.client.force_authenticate(user=self.user)

    def _assert_status_in(self, resp, allowed):
        """Allow either 401 or 403 depending on auth backend configuration."""
        if not isinstance(allowed, (list, tuple, set)):
            allowed = [allowed]
        self.assertIn(
            resp.status_code, allowed,
            f"Expected one of {allowed}, got {resp.status_code} with data={resp.data if hasattr(resp,'data') else resp.content}"
        )

    # -------- Read (Public)

    def test_list_books_anonymous_ok(self):
        url = reverse("book-list")
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        # Expect 3 books
        self.assertEqual(len(resp.data), 3)

    def test_retrieve_book_anonymous_ok(self):
        url = reverse("book-detail", kwargs={"pk": self.book1.pk})
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data["id"], self.book1.id)
        self.assertEqual(resp.data["title"], "1984")
        self.assertEqual(resp.data["publication_year"], 1949)
        self.assertEqual(resp.data["author"], self.author1.id)

    # -------- Create (Auth required)

    def test_create_book_unauth_forbidden(self):
        url = reverse("book-create")
        payload = {"title": "New Book", "publication_year": 2020, "author": self.author1.id}
        resp = self.client.post(url, payload, format="json")
        self._assert_status_in(resp, [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])

    def test_create_book_authenticated_ok(self):
        self._auth()
        url = reverse("book-create")
        payload = {"title": "Down and Out in Paris and London", "publication_year": 1933, "author": self.author1.id}
        resp = self.client.post(url, payload, format="json")
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertEqual(resp.data["title"], payload["title"])
        self.assertEqual(resp.data["publication_year"], payload["publication_year"])
        self.assertEqual(resp.data["author"], self.author1.id)
        self.assertTrue(Book.objects.filter(title=payload["title"]).exists())

    def test_create_book_future_year_invalid(self):
        self._auth()
        url = reverse("book-create")
        future_year = 9999  # intentionally invalid; your serializer should reject future years
        payload = {"title": "Future Book", "publication_year": future_year, "author": self.author1.id}
        resp = self.client.post(url, payload, format="json")
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("publication_year", resp.data)

    # -------- Update (Auth required)

    def test_update_book_unauth_forbidden(self):
        url = reverse("book-update", kwargs={"pk": self.book2.pk})
        payload = {"title": "Animal Farm (Updated)", "publication_year": 1946, "author": self.author1.id}
        resp = self.client.put(url, payload, format="json")
        self._assert_status_in(resp, [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])

    def test_update_book_authenticated_ok(self):
        self._auth()
        url = reverse("book-update", kwargs={"pk": self.book2.pk})
        payload = {"title": "Animal Farm (Updated)", "publication_year": 1946, "author": self.author1.id}
        resp = self.client.put(url, payload, format="json")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.book2.refresh_from_db()
        self.assertEqual(self.book2.title, payload["title"])
        self.assertEqual(self.book2.publication_year, payload["publication_year"])

    # -------- Delete (Auth required)

    def test_delete_book_unauth_forbidden(self):
        url = reverse("book-delete", kwargs={"pk": self.book3.pk})
        resp = self.client.delete(url)
        self._assert_status_in(resp, [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])

    def test_delete_book_authenticated_ok(self):
        self._auth()
        url = reverse("book-delete", kwargs={"pk": self.book3.pk})
        resp = self.client.delete(url)
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Book.objects.filter(pk=self.book3.pk).exists())

    # -------- Filtering

    def test_filter_by_title(self):
        url = reverse("book-list")
        resp = self.client.get(url, {"title": "1984"})
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(len(resp.data), 1)
        self.assertEqual(resp.data[0]["title"], "1984")

    def test_filter_by_publication_year(self):
        url = reverse("book-list")
        resp = self.client.get(url, {"publication_year": 1945})
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(len(resp.data), 1)
        self.assertEqual(resp.data[0]["title"], "Animal Farm")

    def test_filter_by_author(self):
        url = reverse("book-list")
        # Filter by author id
        resp = self.client.get(url, {"author": self.author2.id})
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(len(resp.data), 1)
        self.assertEqual(resp.data[0]["title"], "رقائق القرآن")

    # -------- Searching

    def test_search_by_title(self):
        url = reverse("book-list")
        resp = self.client.get(url, {"search": "Animal"})
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        titles = [b["title"] for b in resp.data]
        self.assertIn("Animal Farm", titles)

    def test_search_by_author_name(self):
        url = reverse("book-list")
        resp = self.client.get(url, {"search": "Orwell"})
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        # Both Orwell books should appear
        titles = {b["title"] for b in resp.data}
        self.assertTrue({"1984", "Animal Farm"}.issubset(titles))

    # -------- Ordering

    def test_ordering_by_title_asc(self):
        url = reverse("book-list")
        resp = self.client.get(url, {"ordering": "title"})
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        returned_titles = [b["title"] for b in resp.data]
        self.assertEqual(returned_titles, sorted(returned_titles))

    def test_ordering_by_publication_year_desc(self):
        url = reverse("book-list")
        resp = self.client.get(url, {"ordering": "-publication_year"})
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        years = [b["publication_year"] for b in resp.data]
        self.assertEqual(years, sorted(years, reverse=True))
