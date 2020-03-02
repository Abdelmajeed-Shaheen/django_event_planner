from rest_framework.permissions import BasePermission

class IsOrganizer(BasePermission):
    def has_object_permission(self, request, view, event_obj):
        return request.user == event_obj.organizer
