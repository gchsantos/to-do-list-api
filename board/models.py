import uuid

from django.db import models
from django.utils import timezone

from .constants import LINE_STATUS


class Task(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=50)
    description = models.TextField(null=True)
    status = models.SmallIntegerField(
        choices=LINE_STATUS.get_status(), default=LINE_STATUS.PENDING
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)


    def get_task_status(self) -> LINE_STATUS:
        return LINE_STATUS(self.status).name

    def update_status(self, status: LINE_STATUS):
        self.status = status
        self.updated_at = timezone.now()
        self.save()