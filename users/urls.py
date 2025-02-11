from django.urls import path
from . import views

urlpatterns = [
    path("admin_login/", views.admin_login),
    path("admin_dashboard/", views.admin_dashboard),
]
