from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from rest_framework.generics import GenericAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.parsers import MultiPartParser, FileUploadParser
from django.contrib.auth.models import User
from komax_app.models import Komax
from .serializers import *
from komax_app.modules.HarnessChartProcessing import HarnessChartReader


# Entry point(temporary)
#TODO: rewrite entry point
def index(request):
    return render(request, 'komax_app/index.html', context={"name": "a"})

class KomaxListView(APIView):
    """
    Get list all komaxes
    Post one/list komax

    * Requires token authentication.
    * All are able to access this view.
    """
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        komaxes = Komax.objects.all()
        komax_serializer = KomaxSerializer(komaxes, context={'request': request}, many=True)

        return Response(komax_serializer.data)

    def post(self, request, *args, **kwargs):
        komax_serializer = KomaxSerializer(data=request.data)
        if komax_serializer.is_valid():
            komax_serializer.save()
            return Response(status=status.HTTP_201_CREATED)

        return Response(komax_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class KomaxDetailView(APIView):
    """
    Get one komax
    Put one komax(update)
    Delete one komax

    * Requires token authentication.
    * All are able to access this view.
    """
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.AllowAny]

    def get_object(self, number):
        try:
            return Komax.objects.get(number=number)
        except Komax.DoesNotExist:
            return None

    def get(self, request, number, *args, **kwargs):
        komax = self.get_object(number)
        komax_serializer = KomaxSerializer(komax, context={'request': request})

        return Response(komax_serializer.data)

    def put(self, request, number, *args, **kwargs):
        komax = self.get_object(number)
        if komax is None:
            return Response(status=status.HTTP_404_NOT_FOUND)

        komax_serializer = KomaxSerializer(komax, data=request.data, context={'request': request})
        if komax.is_valid():
            komax.save()
            return Response(status=status.HTTP_202_ACCEPTED)

        return Response(komax_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, number, *args, **kwargs):
        komax = self.get_object(number)
        if komax is None:
            return Response(status=status.HTTP_404_NOT_FOUND)

        komax.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class KappaListView(ListCreateAPIView):
    """
    Get list kappas
    Create kappas

    * Requires token authentication.
    * All are able to access this view.
    """
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.AllowAny]
    queryset = Kappa.objects.all()
    serializer_class = KappaSerializer

class KappaDetailView(RetrieveUpdateDestroyAPIView):
    """
    Get one kappa
    Put one kappa(update)
    Delete one kappa

    * Requires token authentication.
    * All are able to access this view.
    """
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.AllowAny]
    lookup_field = 'number'
    queryset = Kappa.objects.all()
    serializer_class = KappaSerializer

class HarnessListView(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.AllowAny]
    parser_classes = [MultiPartParser]

    def get(self, request, *args, **kwargs):
        harnesses = Harness.objects.all()
        harness_serializer = HarnessSerializer(harnesses, context={'request': request}, many=True)

        return Response(harness_serializer.data)

    def post(self, request, *args, **kwargs):
        harness_serializer = HarnessSerializer(data=request.data)
        if harness_serializer.is_valid():
            harness_serializer.save()

            reader = HarnessChartReader()
            reader.load_file(request.data['file'])
            reader.read_file_chart()

            harness_number = harness_serializer.data.get('harness_number')

            HarnessChart.save_from_dataframe(
                harness_dataframe=reader.get_dataframe(),
                harness_number=harness_number
            )

            return Response(status=status.HTTP_201_CREATED)

        return Response(harness_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class HarnessDetailView(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.AllowAny]
    parser_classes = [MultiPartParser,]

    def get_object(self, harness_number):
        try:
            return Harness.objects.get(harness_number=harness_number)
        except Komax.DoesNotExist:
            return None

    def get(self, request, harness_number, *args, **kwargs):
        harness = self.get_object(harness_number)
        harness_serializer = HarnessSerializer(harness, context={'request': request})
        return Response(harness_serializer.data)

    def delete(self, request, harness_number, *args, **kwargs):
        harness = self.get_object(harness_number)
        if harness is None:
            return Response(status=status.HTTP_404_NOT_FOUND)

        harness.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class HarnessChartListView(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.AllowAny]

    def get_objects(self, harness_number):
        harness_charts = HarnessChart.objects.filter(harness__harness_number__iexact=harness_number)
        if len(harness_charts):
            return harness_charts
        else:
            return None

    def get(self, request, harness_number, *args, **kwargs):
        harness_charts = self.get_objects(harness_number)

        if harness_number is None:
            return Response(status=status.HTTP_404_NOT_FOUND)

        harness_chart_serializer = HarnessChartSerializer(harness_charts, context={'request': request}, many=True)
        return Response(harness_chart_serializer.data)


"""
@api_view(['GET', 'POST'])
def komax_list(request):
    if request.method == 'GET':
        data = Komax.objects.all()

        serializer = KomaxSerializer(data, context={'request': request}, many=True)

        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = KomaxSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT', 'DELETE'])
def komax_detail(request, pk):
    try:
        student = Komax.objects.get(pk=pk)
    except Komax.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        serializer = KomaxSerializer(student, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        student.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
"""
