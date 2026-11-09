from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):

    def has_object_permission(self, request, view, obj):
        return (
            request.user.is_staff or
            obj.user == request.user
        )

class IsPaymentOwner(BasePermission):

    def has_object_permission(self, request, view, obj):

        return (
            request.user.is_staff or
            obj.booking.user == request.user
        )