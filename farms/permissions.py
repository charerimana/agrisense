from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsSuperUser(BasePermission):
    """
    Allow access only to superusers
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_superuser


class IsOwnerOrSuperUser(BasePermission):
    """
    Object-level permission:
    - Superuser: full access
    - Farmer: access only their own data
    """
    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True

        # Farm
        if hasattr(obj, "owner"):
            return obj.owner == request.user

        # Sensor
        if hasattr(obj, "farm"):
            return obj.farm.owner == request.user

        # SensorReading
        if hasattr(obj, "sensor"):
            return obj.sensor.farm.owner == request.user

        # Notification
        if hasattr(obj, "user"):
            return obj.user == request.user

        return False
