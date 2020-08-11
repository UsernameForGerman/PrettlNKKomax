from rest_framework.permissions import BasePermission
from komax_app.models import Komax

class KomaxIsAuthenticated(BasePermission):

    def has_permission(self, request, view):
        komax_id = request.session.get('komax-id', None)
        return bool(Komax.objects.in_bulk(['{}'.format(komax_id)], field_name='identifier'))
