from rest_framework import permissions

class IsHydroponicSystemOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user

class IsMeasurementOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.system.owner == request.user