from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from .serializers import HarnessSerializer, KomaxSerializer, KappaSerializer, KomaxTerminalSerializer, \
    LaboriousnessSerializer, KomaxStatusSerializer, HarnessChartSerializer, KomaxSealSerializer, KomaxTaskSerializer
from komax_app.models import Harness, HarnessChart, Komax, Kappa, Laboriousness, KomaxTerminal, KomaxStatus, KomaxSeal, \
    KomaxTask
from komax_app.modules.KomaxTaskProcessing import get_komax_task_status_on_komax
from rest_framework.response import Response
from komax_app.modules.HarnessChartProcessing import HarnessChartReader
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_201_CREATED, HTTP_202_ACCEPTED, HTTP_200_OK, \
    HTTP_204_NO_CONTENT, HTTP_404_NOT_FOUND

from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny

class KomaxViewSet(ModelViewSet):
    serializer_class = KomaxSerializer
    queryset = Komax.objects.all()
    lookup_field = 'number'
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

class KappaViewSet(ModelViewSet):
    serializer_class = KappaSerializer
    queryset = Kappa.objects.all()
    lookup_field = 'number'
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

class HarnessViewSet(ModelViewSet):
    serializer_class = HarnessSerializer
    queryset = Harness.objects.all()
    lookup_field = 'harness_number'
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def create(self, request, *args, **kwargs):
        harness_number = self.request.data.get('harness_number', None)
        harness_chart = self.request.data.get('harness_chart', None)
        if harness_number and harness_chart:
            Harness.objects.get_or_create(harness_number=harness_number)

            reader = HarnessChartReader()
            reader.load_file(harness_chart)
            reader.read_file_chart()
            HarnessChart.save_from_dataframe(
                harness_dataframe=reader.get_dataframe(),
                harness_number=harness_number
            )

            return Response(status=HTTP_201_CREATED)

        return Response(status=HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        harness_number = self.request.query_params.get('harness_number', None)
        harness_chart = self.request.data.get('harness_chart', None)
        if harness_number and harness_chart:
            reader = HarnessChartReader()
            reader.load_file(harness_chart)
            reader.read_file_chart()
            HarnessChart.save_from_dataframe(
                harness_dataframe=reader.get_dataframe(),
                harness_number=harness_number
            )

            return Response(status=HTTP_202_ACCEPTED)

        return Response(status=HTTP_400_BAD_REQUEST)

class LabourisnessViewSet(ModelViewSet):
    serializer_class = LaboriousnessSerializer
    queryset = Laboriousness.objects.all()
    lookup_field = 'action'
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

class KomaxTerminalsViewSet(ModelViewSet):
    serializer_class = KomaxTerminalSerializer
    queryset = KomaxTerminal.objects.all()
    lookup_field = 'terminal_name'
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

class KomaxSealViewSet(ModelViewSet):
    serializer_class = KomaxSealSerializer
    queryset = KomaxSeal.objects.all()
    lookup_field = 'seal_name'
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

class KomaxStatusViewSet(ReadOnlyModelViewSet):
    serializer_class = KomaxStatusSerializer
    queryset = KomaxStatus.objects.all()
    lookup_field = 'komax'
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

class HarnessChartViewSet(ReadOnlyModelViewSet):
    serializer_class = HarnessChartSerializer
    queryset = HarnessChart.objects.all()
    lookup_field = 'harness_number'
    permission_classes = [AllowAny]
    authentication_classes = [TokenAuthentication]

    def retrieve(self, request, *args, **kwargs):
        harness_number = self.kwargs.get('harness_number', None)
        if harness_number is not None:
            harness_chart_objs = HarnessChart.objects.filter(harness__harness_number=harness_number)
            if len(harness_chart_objs):
                serializer = HarnessChartSerializer(harness_chart_objs, many=True)

                return Response(serializer.data, status=HTTP_200_OK)
            return Response(status=HTTP_204_NO_CONTENT)
        return Response(status=HTTP_400_BAD_REQUEST)

# class KomaxTaskViewSet(ModelViewSet):
#     serializer_class = KomaxTask
#     queryset = KomaxTask.objects.all()
#     lookup_field = 'task_name'
#     permission_classes = [AllowAny]
#     authentication_classes = [TokenAuthentication]
#
#     def list(self, request, *args, **kwargs):
#         komax_task_serializer = KomaxTaskSerializer(KomaxTask.objects.all(), many=True)
#         return Response(komax_task_serializer.data, status=HTTP_200_OK)
#
#         user = self.request.user
#         if user.groups.filter(name='Master').exists():
#             if len(self.queryset):
#                 komax_task_serializer = KomaxTaskSerializer(self.queryset, context={'request': self.request})
#                 return Response(komax_task_serializer.data, status=HTTP_200_OK)
#             else:
#                 return Response(status=HTTP_204_NO_CONTENT)
#         elif user.groups.filter(name='Operator').exists():
#             komax = user.current_komax
#             komax_number = komax.number if komax is not None else None
#             if komax_number is None:
#                 return Response(status=HTTP_404_NOT_FOUND)
#             if len(self.queryset):
#                 for obj in self.queryset:
#                     obj.status = get_komax_task_status_on_komax(obj, komax_number)
#                 komax_task_serializer = KomaxTaskSerializer(self.queryset, context={'request': self.request})
#                 return Response(komax_task_serializer.data, status=HTTP_200_OK)
#             else:
#                 return Response(status=HTTP_204_NO_CONTENT)
#         else:
#             return Response(status=HTTP_400_BAD_REQUEST)



