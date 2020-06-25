from rest_framework.permissions import BasePermission
from komax_app.models import Komax

class KomaxIsAuthenticated(BasePermission):

    def has_permission(self, request, view):
        komax_ids = Komax.objects.all().values_list('identifier', flat=True)
        return bool('komax-id' in request.session and request.session.get('komax-id') in komax_ids)
