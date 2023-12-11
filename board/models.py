import uuid

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

from .constants import TASK_STATUS


class Task(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=50)
    description = models.TextField(null=True)
    status = models.SmallIntegerField(
        choices=TASK_STATUS.get_status(), default=TASK_STATUS.PENDING
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="tasks"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)


    def get_task_status(self) -> TASK_STATUS:
        return TASK_STATUS(self.status).name

    def update_status(self, status: TASK_STATUS):
        self.status = status
        self.updated_at = timezone.now()
        self.save()