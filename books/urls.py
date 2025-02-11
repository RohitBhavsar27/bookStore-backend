from django.urls import path
from . import views

urlpatterns = [
    path("addBook/", views.addBook),
    path("getAllBooks/", views.getAllBooks),
    path("getBook/<book_id>", views.getBook),
    path("updateBook/<book_id>", views.updateBook),
    path("deleteBook/<book_id>", views.deleteBook),
]
