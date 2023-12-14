import uuid

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class TaskStatus(models.IntegerChoices):
    PENDING = 1, "The task is pending"
    CONCLUDED = 2, "The task has been completed"
    CANCELED = 3, "The task was canceled"

    @classmethod
    def get_status_by_name(cls, label: str):
        return cls._member_map_[label.upper()]


class Task(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=50)
    description = models.TextField(null=True)
    status = models.SmallIntegerField(
        choices=TaskStatus.choices, default=TaskStatus.PENDING
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="tasks"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)

    @property
    def task_status(self) -> TaskStatus:
        return TaskStatus(self.status)

    def update_status(self, status: TaskStatus):
        if self.status != status:
            self.status = status
            self.updated_at = timezone.now()
            self.save()

    class Meta:
        constraints = [
            models.CheckConstraint(
                name="%(app_label)s_%(class)s_status_valid",
                check=models.Q(status__in=TaskStatus.values),
            )
        ]
