from django.shortcuts import render, redirect
from .models import Post
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm


def index(request):
    posts = Post.objects.all().order_by('-published_date')
    return render(request, "blog/index.html", {"posts": posts})



# Registration view
def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # auto login after registration
            return redirect("profile")
    else:
        form = RegisterForm()
    return render(request, "blog/register.html", {"form": form})

# Profile view
@login_required
def profile(request):
    if request.method == "POST":
        request.user.email = request.POST.get("email")
        request.user.save()
        return redirect("profile")
    return render(request, "blog/profile.html")
