from django.urls import path
from . import views

urlpatterns = [
    path("getNewsData/", views.getNewsData),
]
