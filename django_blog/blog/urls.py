from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),

    path("register/", views.register, name="register"),
    path("profile/", views.profile, name="profile"),

    path("post/new/", views.PostCreateView.as_view(), name="post_create"),
    path("post/<int:pk>/", views.PostDetailView.as_view(), name="post_detail"),
    path("post/<int:pk>/update/", views.PostUpdateView.as_view(), name="post_update"),
    path("post/<int:pk>/delete/", views.PostDeleteView.as_view(), name="post_delete"),
]
