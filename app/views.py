import re
from django.shortcuts import get_object_or_404, render, redirect
from .models import Blog, Feature, TechStack
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
        try:
            if form.is_valid():
                form.save()
                messages.success(request, "Project added successfully!")
                return redirect("home")
            else:
                # Get form errors as messages
                for field in form.errors:
                    for error in form.errors[field]:
                        messages.error(request, f"{field}: {error}")
                messages.error(request, "Please correct the errors below...")
        except Exception as e:
            messages.error(request, f"Error saving project: {str(e)}")
    else:
        form = BlogForm()

    context = {"form": form}
    return render(request, "add.html", context)


def delete(request, id):
    blog = get_object_or_404(Blog, id=id)
    if request.method == "POST":
        blog.delete()
        messages.success(request, "Project deleted successfully!")
        return redirect("home")
    context = {"blog": blog}

    return render(request, "delete.html", context)


def edit(request, id):
    try:
        blog = Blog.objects.get(id=id)
    except Blog.DoesNotExist:
        messages.error(request, "Project not found!")
        return redirect("home")

    if request.method == "POST":
        form = BlogForm(request.POST, request.FILES, instance=blog)
        if form.is_valid():
            form.save()
            messages.success(request, "Project updated successfully!")
            return redirect("home")
        else:
            messages.error(request, "Please correct the errors below...")
    else:
        form = BlogForm(instance=blog)

    context = {"form": form, "blog": blog}
    return render(request, "add.html", context)


def search(request):
    return render(request, "search.html")
