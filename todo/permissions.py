from rest_framework import permissions


class TaskPermissions(permissions.BasePermission):
    """Проверка прав для задач.
    Для созданий задачи проверят на группу employee.
    Для остальных не безопасных методов проверят на владельца или на группу админ.
    В безопасных методах возвращает True, проверка на авторизацию делается 
    проверкой в предствлений IsAuthenticated"""

    def has_permission(self, request, view):
        """ Проверят права для создания задач
        во всех остальных случаях разрешает"""
        if request.method in permissions.SAFE_METHODS:
            return True

        if request.method == 'POST':
            return request.user.groups.filter(name='employee').exists()
        
        return True

    def has_object_permission(self, request, view, obj):
        """ Проверка на уровне объекта
        проверяет на владелеца задачи или группа админ"""
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.owner == request.user or request.user.groups.filter(name='admin').exists()
