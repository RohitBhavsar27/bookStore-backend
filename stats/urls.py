from django.urls import path
from . import views

urlpatterns = [
    path('stats/',views.admin_stats)
]
