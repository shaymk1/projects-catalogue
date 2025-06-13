from django.shortcuts import get_object_or_404, render, redirect
from .models import Blog
from .forms import BlogForm
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q


def home(request):

    # search functionality
    search_query = request.GET.get("q", "")
    blogs = Blog.objects.all().order_by("-created_at")
    if search_query:
        blogs = blogs.filter(
            Q(title__icontains=search_query) |
            Q(content__icontains=search_query) |
            Q(features__name__icontains=search_query) |
            Q(tech_stack__name__icontains=search_query)
        ).distinct()
    if not blogs:
        messages.warning(request, "No results found for your search query.")
    # pagination
    paginator = Paginator(blogs, 6)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    context = {
        "page_obj": page_obj,
        "search_query": search_query,
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
    blog = get_object_or_404(Blog, id=id)
    if request.method == "POST":
        form = BlogForm(request.POST, request.FILES, instance=blog)
        if form.is_valid():
            form.save()
            messages.success(request, "Project updated successfully!")
            return redirect("home")
        else:
            # Get form errors as messages
            for field in form.errors:
                for error in form.errors[field]:
                    messages.error(request, f"{field}: {error}")
            messages.error(request, "Please correct the errors below...")
    else:
        form = BlogForm(instance=blog)
    context = {"form": form, "blog": blog}
    return render(request, "edit.html", context)


def search(request):
    return render(request, "search.html")
