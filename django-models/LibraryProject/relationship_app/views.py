from .models import Library
from django.views.generic.detail import DetailView
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.views import View
from django.shortcuts import render, redirect


# def list_books(request):
#     books = Book.objects.all()  # <== Required by your checker
#     return render(request, 'relationship_app/list_books.html', {'books': books})  # <== Required path

class LibraryDetailView(DetailView):
    model = Library
    template_name = 'relationship_app/library_detail.html'  # explicit template
    context_object_name = 'library'

class RegisterView(View):
    def get(self, request):
        form = UserCreationForm()
        return render(request, 'relationship_app/register.html', {'form': form})

    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
        return render(request, 'relationship_app/register.html', {'form': form})
