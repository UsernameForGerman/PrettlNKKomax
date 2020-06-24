# django libs imports
from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.parsers import MultiPartParser
from django.utils.decorators import method_decorator
from django.contrib.auth.models import AnonymousUser
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_201_CREATED, HTTP_202_ACCEPTED, HTTP_200_OK, \
    HTTP_204_NO_CONTENT, HTTP_404_NOT_FOUND, HTTP_409_CONFLICT

# customs
from django_pandas.io import read_frame
import pandas as pd
from drf_renderer_xlsx.mixins import XLSXFileMixin
from drf_renderer_xlsx.renderers import XLSXRenderer

# local imports
from komax_app.models import Komax, Worker
from .serializers import *
from komax_app.models import KomaxOrder
from komax_app.modules.HarnessChartProcessing import HarnessChartReader
from komax_app.modules.KomaxTaskProcessing import get_komax_task_status_on_komax, KomaxTaskProcessing, \
    update_komax_task_status
from komax_app.modules.outer import OutProcess



# Entry point(temporary)
#TODO: rewrite entry point
def index(request):
    return render(request, 'komax_app/index.html', context={"name": "a"})

# class XlsxTaskView(APIView):
#     """
#     Get xlsx document of full task, and task on each komax
#     """
#
#     authentication_classes = (TokenAuthentication, )
#     # permission_classes = (IsAuthenticated, )
#     permission_classes = (AllowAny,)
#     # renderer_classes = (XLSXRenderer, )
#
#     def get(self, request, *args, **kwargs):
#         task_name = self.request.query_params.get('task-name', None)
#         if not task_name:
#             return Response('No komax task name provided', status=HTTP_400_BAD_REQUEST)
#
#         komax = self.request.query_params.get('komax', None)
#         if komax:
#             pass
#         else:
#             task_pers_df = read_frame(
#                 TaskPersonal.objects.filter(komax_task=get_object_or_404(KomaxTask, task_name=task_name)))
#
#             task_pers_df.sort_values(
#                 by=['id'],
#                 ascending=True,
#                 inplace=True,
#             )
#
#             task_pers_df.drop(labels='worker', axis='columns', inplace=True)
#             task_pers_df.index = pd.Index(range(task_pers_df.shape[0]))
#
#             task_pers_df['done'] = ''
#
#             response = Response(
#                 content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
#                 status=HTTP_200_OK,
#             )
#             response['Content-Disposition'] = 'attachment; filename={task_name}.xlsx'.format(
#                 task_name=task_name,
#             )
#
#             out_file = OutProcess(task_pers_df)
#             workbook = out_file.get_task_xl()
#             ws = workbook.active
#             workbook.save(response)
#
#             return response

class SendTaskView(APIView):
    """
    Send tasks to workers
    """
    permission_classes = (IsAuthenticated, )
    authentication_classes = (TokenAuthentication, )

    def put(self, task_name, *args, **kwargs):
        task_obj = get_object_or_404(KomaxTask, task_name=task_name)
        task_obj.status = 2
        task_obj.save(update_fields=['status'])

        return Response(status=HTTP_200_OK)

class LoadTaskView(APIView):
    """
    Load tasks into komax
    """
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated, )

    def put(self, task_name, *args, **kwargs):
        komax_num = self.request.session.get('komax', None)
        komax = get_object_or_404(Komax, number=komax_num)
        komax_task = get_object_or_404(KomaxTask, task_name=task_name)
        old_komax_tasks_id = TaskPersonal.objects.filter(
            loaded=True,
            komax=komax
        ).exclude(
            komax_task=komax_task
        ).values_list(
            'komax_task',
            flat=True
        ).distinct()

        old_komax_tasks = KomaxTask.objects.filter(id__in=old_komax_tasks_id).values_list('taks_name', flat=True)
        if len(old_komax_tasks):
            return Response(
                'Stop {} komax tasks before loading new one'.format(', '.join(old_komax_tasks)),
                status=HTTP_409_CONFLICT
            )
        processor = KomaxTaskProcessing()
        processor.load_task_personal(task_name, komax_num)
        KomaxOrder.objects.create(komax_task=komax_task, komax=komax, status='Received')

        update_komax_task_status(komax_task)

        return Response(status=HTTP_200_OK)

class KomaxListView(APIView):
    """
    Get list all komaxes
    Post one/list komax

    * Requires token authentication.
    """
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated, )

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
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated, )

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
        if komax_serializer.is_valid():
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
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated, )
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
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated, )
    lookup_field = 'number'
    queryset = Kappa.objects.all()
    serializer_class = KappaSerializer

class HarnessListView(APIView):
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated, )
    parser_classes = [MultiPartParser]

    def get(self, request, *args, **kwargs):
        harnesses = Harness.objects.all()
        harness_serializer = HarnessSerializer(harnesses, context={'request': request}, many=True)

        return Response(harness_serializer.data)

    def post(self, request, *args, **kwargs):
        harness_chart_xlsx_serializer = HarnessChartXlsxSerializer(data=request.data)
        harness_chart = request.data['file']
        if harness_chart_xlsx_serializer.is_valid():

            harness_number = harness_chart_xlsx_serializer.data['harness_number']
            # harness_chart = harness_chart_xlsx_serializer.data['file']
            # print(harness_chart)
            Harness.objects.create(harness_number=harness_number)

            reader = HarnessChartReader()
            reader.load_file(harness_chart)
            reader.read_file_chart()
            HarnessChart.save_from_dataframe(
                harness_dataframe=reader.get_dataframe(),
                harness_number=harness_number
            )

            return Response(status=status.HTTP_201_CREATED)


        return Response(harness_chart_xlsx_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class HarnessDetailView(APIView):
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated, )
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
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated, )

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

class KomaxTaskListView(APIView):
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated, )
    queryset = KomaxTask.objects.all()

    def get_object(self, task_name=None):
        if task_name:
            return KomaxTask.objects.filter(task_name=task_name)
        else:
            return KomaxTask.objects.all()

    def get_queryset(self):
        return KomaxTask.objects.all()

    def get(self, request, *args, **kwargs):
        user = self.request.user
        if user.groups.filter(name='Master').exists():
            queryset = self.get_queryset()
            if len(queryset):
                komax_task_serializer = KomaxTaskSerializer(queryset, context={'request': self.request}, many=True)
                return Response(komax_task_serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_204_NO_CONTENT)
        elif user.groups.filter(name='Operator').exists():
            queryset = self.get_queryset()
            worker = Worker.objects.get(user=user)
            komax = worker.current_komax
            komax_number = komax.number if komax is not None else None
            if komax_number is None:
                return Response(status=status.HTTP_404_NOT_FOUND)
            if len(queryset):
                for obj in queryset:
                    obj.status = get_komax_task_status_on_komax(obj, komax_number)
                    for komax_time in obj.komaxes.exclude(komax=komax):
                        obj.komaxes.remove(komax_time)
                komax_task_serializer = KomaxTaskSerializer(queryset, context={'request': self.request}, many=True)
                return Response(komax_task_serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, *args, **kwargs):
        data = self.request.data
        komax_task_name = data.get('task_name', None)
        harnesses = data.get('harnesses', None)
        komaxes = data.get('komaxes', None)
        kappas = data.get('kappas', None)
        shift = data.get('shift', None)
        type_of_allocation = data.get('type_of_allocation', None)
        loading_type = data.get('loading_type', None)
        print(data)
        if komax_task_name:
            komax_task = self.get_object(komax_task_name)
            if not len(komax_task) and harnesses and komaxes and shift and type_of_allocation and loading_type:
                komax_task_processor = KomaxTaskProcessing()
                komax_task_processor.create_komax_task(
                    komax_task_name,
                    harnesses,
                    komaxes,
                    kappas,
                    shift,
                    type_of_allocation,
                    loading_type
                )
                komax_task_processor.sort_save_komax_task(komax_task_name)
                return Response(status=status.HTTP_200_OK)
            elif len(komax_task):
                harness_amount_dict = data.get('harness_amount', None)
                if harness_amount_dict:
                    komax_task_processor = KomaxTaskProcessing()
                    komax_task_processor.update_harness_amount(komax_task_name, harness_amount_dict)
                    allocation = komax_task_processor.create_allocation(komax_task_name)
                    komax_task_processor.update_komax_time(
                        komax_task_name,
                        {komax: time[0] for komax, time in allocation.items()}
                    )
                    return Response(status=status.HTTP_200_OK)
                else:
                    return Response(status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(status=status.HTTP_204_NO_CONTENT)

        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

class Logout(APIView):

    def get(self, request, format=None):
        user = request.user
        if user is not AnonymousUser:
            if user.groups.filter(name='Operator'):
                worker = get_object_or_404(Worker, user=user)
                worker.current_komax = None
                worker.save()

        # simply delete the token to force a login
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)


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
