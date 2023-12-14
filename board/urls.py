from django.urls import path, re_path

from .views import BoardManager
from to_do_list_api.constants import UUID_REGEX

urlpatterns = [
    path("", BoardManager.as_view(), name="Board Manager"),
    re_path(
        rf"^/(?P<task_id>{UUID_REGEX})",
        BoardManager.as_view(),
        name="Board Manager",
    ),
]
