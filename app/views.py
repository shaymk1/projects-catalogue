import re
from django.shortcuts import render, redirect
from .models import Blog
from .forms import BlogForm
from django.contrib import messages


def home(request):
    blogs = Blog.objects.all().order_by("-created_at")
    context = {
        "blogs": blogs,
    }
    return render(request, "index.html", context)


def detailed(request, id):
    blog = Blog.objects.get(id=id)
    context = {"blog": blog}
    return render(request, "detailed.html", context)


def add(request):
    if request.method == "POST":
        form = BlogForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Project added successfully!")
            return redirect("home")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = BlogForm()

    return render(request, "add.html", {"form": form})


def delete(request, id):
    return render(request, "delete.html")


def edit(request, id):
    return render(request, "edit.html")


def search(request):
    return render(request, "search.html")
