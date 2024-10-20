from django.urls import path
from django.views.generic import RedirectView

from . import views

app_name = 'wiki'
urlpatterns = [
    path('', RedirectView.as_view(url='wiki')),
    path("wiki", views.index, name="index"),
    path("wiki/<str:title>", views.title, name="title"),
    path("search/", views.search, name="search"),
    path("random/", views.random_page, name="random"),
    path("create/", views.create_page, name="create"),
    path("edit/<str:title>", views.edit_page, name="edit"),
    path("delete/<str:title>", views. delete_page, name="delete"),
]