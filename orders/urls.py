from django.urls import path
from . import views

urlpatterns = [
    path("newOrder/", views.newOrder),
    path("getOrder/<email>", views.getOrder),
]
