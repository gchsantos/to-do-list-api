from rest_framework import serializers

from .models import Task, TaskStatus


class UserTasksSerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField()
    statusLabel = serializers.SerializerMethodField()
    createdAt = serializers.DateTimeField(source="created_at")
    updatedAt = serializers.DateTimeField(source="updated_at")

    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'status', 'statusLabel',
                  'createdAt', 'updatedAt']
        
    def get_status(self, instance):
        return TaskStatus(instance.status).name
    
    def get_statusLabel(self, instance):
        return TaskStatus(instance.status).label
