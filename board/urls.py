from django.urls import path

from .views import BoardManager

urlpatterns = [
    path("", BoardManager.as_view(), name="Board Manager"),
]