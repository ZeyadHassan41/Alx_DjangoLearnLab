from django.urls import path
from .views import LibraryDetailView

urlpatterns = [
    path('library/<int:pk>/', LibraryDetailView.as_view(), name='library-detail'),
]
