from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("add/", views.add, name="add"),
    path("detailed/<int:id>/", views.detailed, name="detailed"),
    path("edit/<int:id>/", views.edit, name="edit"),
    path("delete/<int:id>/", views.delete, name="delete"),
    path("search/", views.search, name="search"),
]
