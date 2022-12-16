from rest_framework import permissions, exceptions
from accounts.models import HNUser
from rest_framework_api_key.permissions import BaseHasAPIKey
from .models import UserAPIKey

class ApiKeyUserOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the snippet.
        try:
            key = request.META["HTTP_AUTHORIZATION"].split()[1]
            user = HNUser.objects.get(key=key)
            return obj.user == user
        except KeyError: 
            raise exceptions.NotAuthenticated(detail="Api-Key credentials were not provided.")
        except HNUser.DoesNotExist:
            raise exceptions.NotFound(detail="Api-Key has no user associated", code=410)
        return False

# Indica que model usar para las API Keys
class HasAPIKey(BaseHasAPIKey):
    model = UserAPIKey