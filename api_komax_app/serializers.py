from rest_framework.serializers import ModelSerializer
from komax_app.models import Komax, Kappa, KomaxTask, TaskPersonal, Laboriousness, KomaxTerminal, Harness, \
    HarnessChart


class KomaxSerializer(ModelSerializer):
    class Meta:
        model = Komax
        fields = ('number', 'identifier', 'status', 'marking', 'pairing', 'group_of_square')

class KappaSerializer(ModelSerializer):
    class Meta:
        model = Kappa
        fields = '__all__'

class HarnessSerializer(ModelSerializer):
    class Meta:
        model = Harness
        fields = '__all__'

class HarnessChartSerializer(ModelSerializer):
    class Meta:
        model = HarnessChart
        fields = '__all__'

class EquipmentSerializer(ModelSerializer):
    komaxes = KomaxSerializer()
    kappas = KappaSerializer()




