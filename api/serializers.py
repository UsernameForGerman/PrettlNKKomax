from rest_framework.serializers import ModelSerializer, Serializer, FileField, CharField, IntegerField
from django.contrib.auth.models import Group
from komax_app.models import Komax, Kappa, KomaxTask, TaskPersonal, Laboriousness, KomaxTerminal, Harness, \
    HarnessChart, KomaxStatus, KomaxSeal, KomaxTime, HarnessAmount, Worker, KomaxTaskCompletion


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
        fields = ('harness_number', 'created')

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

class KomaxTimeSerializer(ModelSerializer):
    class Meta:
        model = KomaxTime
        fields = '__all__'

    # def to_representation(self, value):
    #     data = super(KomaxTimeSerializer, self).to_representation(value)
    #     return data

class HarnessAmountSerializer(ModelSerializer):
    class Meta:
        model = HarnessAmount
        fields = '__all__'

    # def to_representation(self, value):
    #     data = super(HarnessAmountSerializer, self).to_representation(value)
    #     return data

class KomaxTaskSerializer(ModelSerializer):
    komaxes = KomaxTimeSerializer(read_only=True, many=True)
    harnesses = HarnessAmountSerializer(read_only=True, many=True)


    class Meta:
        model = KomaxTask
        fields = ('task_name', 'komaxes', 'harnesses', 'status')

class WorkerSerializer(ModelSerializer):
    class Meta:
        model = Worker
        fields = '__all__'

class HarnessCompletionSerializer(Serializer):
    harness_number = CharField(max_length=256)
    left_time_secs = IntegerField()
    sum_time_secs = IntegerField()

class KomaxTaskCompletionSerializer(Serializer):
    harnesses = HarnessCompletionSerializer(many=True, read_only=True)
    task_name = CharField(max_length=256, read_only=True)



class UserGroupsSerializer(ModelSerializer):
    class Meta:
        model = Group
        fields = ('name', )



