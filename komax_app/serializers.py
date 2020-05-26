from rest_framework import serializers
from .models import Komax


class KomaxSerializer(serializers.ModelSerializer):
    class Meta:
        model = Komax
        fields = ('number', 'identifier', 'status', 'marking', 'pairing', 'group_of_square')
