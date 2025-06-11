from django.shortcuts import render
from .models import Blog


def home(request):
    blogs = Blog.objects.all().order_by("-created_at")
    context = {
        "blogs": blogs,
    }
    return render(request, "index.html", context)
