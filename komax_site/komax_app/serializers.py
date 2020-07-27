from rest_framework import serializers
from .models import Komax, Harness


class KomaxSerializer(serializers.ModelSerializer):
    class Meta:
        model = Komax
        fields = ('number', 'identifier', 'status', 'marking', 'pairing', 'group_of_square')

class HarnessSerializer(serializers.ModelSerializer):
    class Meta:
        model = Harness
        fields = ('created', 'harness_number')
