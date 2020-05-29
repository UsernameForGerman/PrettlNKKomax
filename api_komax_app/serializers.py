from rest_framework.serializers import ModelSerializer, Serializer, FileField, CharField
from komax_app.models import Komax, Kappa, KomaxTask, TaskPersonal, Laboriousness, KomaxTerminal, Harness, \
    HarnessChart, KomaxStatus, KomaxSeal


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

class HarnessChartXlsxSerializer(Serializer):
    file = FileField()
    harness_number = CharField()


class EquipmentSerializer(ModelSerializer):
    komaxes = KomaxSerializer()
    kappas = KappaSerializer()

class LaboriousnessSerializer(ModelSerializer):
    class Meta:
        model = Laboriousness
        fields = '__all__'

class KomaxTerminalSerializer(ModelSerializer):
    class Meta:
        model = KomaxTerminal
        fields = '__all__'

class KomaxStatusSerializer(ModelSerializer):
    class Meta:
        model = KomaxStatus
        fields = '__all__'

class KomaxSealSerializer(ModelSerializer):
    class Meta:
        model = KomaxSeal
        fields = '__all__'




