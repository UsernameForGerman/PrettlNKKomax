from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from .serializers import HarnessSerializer, KomaxSerializer, KappaSerializer, KomaxTerminalSerializer, \
    LaboriousnessSerializer, KomaxStatusSerializer, HarnessChartSerializer, KomaxSealSerializer
from komax_app.models import Harness, HarnessChart, Komax, Kappa, Laboriousness, KomaxTerminal, KomaxStatus, KomaxSeal
from rest_framework.response import Response
from komax_app.modules.HarnessChartProcessing import HarnessChartReader
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_201_CREATED, HTTP_202_ACCEPTED, HTTP_200_OK, \
    HTTP_204_NO_CONTENT

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
    permission_classes = [IsAuthenticated]
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


