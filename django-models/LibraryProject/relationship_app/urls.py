from django.urls import path
from .views import RegisterView
from django.contrib.auth.views import LoginView, LogoutView
from . import views


urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(template_name='relationship_app/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='relationship_app/logout.html'), name='logout'),
    path('books/', views.book_list, name='book-list'),  # Example
]
