from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import Task
from .serializers import TaskSerializer
from .permissions import TaskPermissions


class TaskViewSet(viewsets.ModelViewSet):
    """Набор представлений для задач"""
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated, TaskPermissions]
