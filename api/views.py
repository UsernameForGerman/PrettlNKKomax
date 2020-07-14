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
from django.shortcuts import get_object_or_404, get_list_or_404, HttpResponse
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_201_CREATED, HTTP_202_ACCEPTED, HTTP_200_OK, \
    HTTP_204_NO_CONTENT, HTTP_404_NOT_FOUND, HTTP_409_CONFLICT, HTTP_401_UNAUTHORIZED

# customs
from django_pandas.io import read_frame
import pandas as pd

# local imports
from komax_app.models import Komax, Worker
from .serializers import *
from komax_app.models import KomaxOrder, KomaxTaskCompletion, KomaxTask, TaskPersonal, Kappa, Komax,HarnessChart, Harness, KomaxStatus
from komax_app.modules.HarnessChartProcessing import HarnessChartReader
from komax_app.modules.KomaxTaskProcessing import get_komax_task_status_on_komax, KomaxTaskProcessing, \
    update_komax_task_status, stop_komax_task_on_komax
from komax_app.modules.outer import OutProcess



# Entry point(temporary)
#TODO: rewrite entry point
def index(request):
    return render(request, 'komax_app/index.html', context={"name": "a"})

class KomaxTaskStop(APIView):
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated, )

    def post(self, *args, **kwargs):
        task_name = self.kwargs.get('task_name', None)
        task_obj = get_object_or_404(KomaxTask, task_name=task_name)
        for komax in task_obj.komaxes.all():
            stop_komax_task_on_komax(komax.komax, task_obj)
            if TaskPersonal.objects.filter(komax=komax.komax, loaded=True, komax_task=task_obj).exists():
                KomaxOrder.objects.create(komax_task=task_obj, komax=komax.komax, status="Requested")
            else:
                pass

        return Response(status=HTTP_200_OK)

class KomaxTaskStopOnKomax(APIView):
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated, )

    def post(self, *args, **kwargs):
        task_name = self.kwargs.get('task_name', None)
        komax = self.kwargs.get('komax', None)
        worker = get_object_or_404(Worker, user=self.request.user)
        if int(komax) != int(worker.current_komax.number):
            return Response(status=HTTP_404_NOT_FOUND)

        komax_task = get_object_or_404(KomaxTask, task_name=task_name)
        komax = worker.current_komax
        stop_komax_task_on_komax(komax, komax_task)
        if TaskPersonal.objects.filter(komax=komax, loaded=True, komax_task=komax_task).exists():
            KomaxOrder.objects.create(komax_task=komax_task, komax=komax, status="Requested")
        else:
            pass

        return Response(status=HTTP_200_OK)

class WorkerAccountView(APIView):
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated, )

    def get(self, request, *args, **kwargs):
        worker = get_object_or_404(Worker, user=request.user)
        if worker.user.groups.filter(name='Operator').exists():
            komax = worker.current_komax
            if komax is None:
                return Response('No komax number provided', status=HTTP_404_NOT_FOUND)

            ordered_komax_tasks = KomaxTask.objects.filter(
                komaxes__komax=komax,
            ).exclude(
                status=1
            ).order_by(
                '-created'
            )
            response_data = KomaxTaskSerializer(ordered_komax_tasks, many=True).data

            return Response(response_data, status=HTTP_200_OK)
        elif worker.user.groups.filter(name='Master').exists():
            komax_task_objs = get_list_or_404(KomaxTask, status=3)
            response_data = KomaxTaskSerializer(komax_task_objs, many=True).data

            return Response(response_data, status=HTTP_200_OK)
        else:
            return Response('No user group', status=HTTP_404_NOT_FOUND)

class SendTaskView(APIView):
    """
    Send tasks to workers
    """
    permission_classes = (IsAuthenticated, )
    authentication_classes = (TokenAuthentication, )

    def put(self, *args, **kwargs):
        task_name = self.request.data.get('task_name', None)
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

    def put(self, *args, **kwargs):
        task_name = self.request.data.get('task_name', None)
        # user = self.request.data.get('username', None)
        # worker = Worker.objects.filter(user__username=user).first()
        user = self.request.user
        worker = get_object_or_404(Worker, user=user)
        komax = worker.current_komax
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

        old_komax_tasks = KomaxTask.objects.filter(id__in=old_komax_tasks_id).values_list('task_name', flat=True)
        if len(old_komax_tasks):
            return Response(
                'Stop {} komax tasks before loading new one'.format(', '.join(old_komax_tasks)),
                status=HTTP_409_CONFLICT
            )
        processor = KomaxTaskProcessing()
        processor.load_task_personal(task_name, komax.number)
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

class Logout(APIView):

    def delete(self, *args, **kwargs):
        user = self.request.user
        if user is not AnonymousUser:
            if user.groups.filter(name='Operator'):
                worker = get_object_or_404(Worker, user=user)
                worker.current_komax = None
                worker.save()

        self.request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)

class TaskStatusView(APIView):
    permission_classes = (IsAuthenticated, )
    authentication_classes = (TokenAuthentication, )

    def get(self, *args, **kwargs):
        # task_name = self.request.query_params.get('task-name', '')
        # if task_name:
        #     task_obj = get_object_or_404(KomaxTask, task_name=task_name)
        task_obj = get_object_or_404(KomaxTask, status=3)
        komax_status_queryset = KomaxStatus.objects.all()

        komax_task_df = read_frame(TaskPersonal.objects.filter(komax_task=task_obj))
        print(komax_task_df)
        print(komax_task_df.shape)
        komax_idx_dict = dict()

        for komax_time in task_obj.komaxes.all():
            print(komax_time)
            komax_status_obj = komax_status_queryset.filter(komax=komax_time.komax).first()
            print(komax_status_obj)
            if komax_status_obj and komax_status_obj.task_personal:
                idx = komax_status_obj.task_personal.id
                komax_idx_dict[komax_status_obj.komax.number] = idx
            else:
                komax_idx_dict[komax_time.komax.number] = 0

        harnesses = komax_task_df['harness'].unique()
        komax_task_completion_data = {
            'komax_task': task_obj,
            'harnesses': []
        }
        for harness in harnesses:
            left_times = [
                sum(
                    komax_task_df[(komax_task_df['id'] > idx) & (komax_task_df['harness'] == harness) & (
                            komax_task_df['komax'] == str(komax))][
                        'time']) if idx is not None else 0 for komax, idx in komax_idx_dict.items()
            ]

            sum_all_times = [
                sum(komax_task_df[
                        (komax_task_df['harness'] == harness) & (komax_task_df['komax'] == str(komax))][
                        'time']) if idx is not None else 0 for komax, idx in komax_idx_dict.items()
            ]
            print(harness)
            print(komax_idx_dict)
            print(left_times)
            print(sum_all_times)

            if len(left_times) and len(sum_all_times):
                data = {
                    'number': harness,
                    'percent': round((1 - sum(left_times) / sum(sum_all_times)) * 100) if sum(sum_all_times) > 0 else 0,
                    'left': max(left_times),
                    'all': sum(sum_all_times) if sum(sum_all_times) > 0 else 0,
                }
            else:
                data = {
                    'number': harness,
                    'percent': 0,
                    'left': 0,
                    'all': 0,
                }

            komax_task_completion_data['harnesses'].append({
                'harness_number': data['number'],
                'left_time_secs': data['left'],
                'sum_time_secs': data['all']
            })

        print(komax_task_completion_data)
        response_data = KomaxTaskCompletionSerializer(komax_task_completion_data).data
        print(response_data)
        return Response(response_data, status=HTTP_200_OK)

class UserGroupView(APIView):
    permission_classes = (IsAuthenticated, )
    authentication_classes = (TokenAuthentication, )

    def get(self, *args, **kwargs):
        response_data = UserGroupsSerializer(self.request.user.groups.all(), many=True).data
        return Response(response_data, status=HTTP_200_OK)

# @login_required
# @permission_required('komax_app.view_komaxtask')
def get_personal_task_view_komax(request, task_name, komax):
    komax_obj = get_object_or_404(Komax, number=komax)
    tasks_obj = get_object_or_404(KomaxTask, task_name=task_name)
    task_pers_df = read_frame(TaskPersonal.objects.filter(komax_task=tasks_obj, komax=komax_obj))

    task_pers_df.sort_values(
        by=['id'],
        ascending=True,
        inplace=True,
    )

    task_pers_df.drop(labels='worker', axis='columns', inplace=True)
    task_pers_df.index = pd.Index(range(task_pers_df.shape[0]))

    task_pers_df['done'] = ''

    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    )
    response['Content-Disposition'] = 'attachment; filename={task_name}-{komax_number}.xlsx'.format(
        task_name=task_name,
        komax_number=komax,
    )

    out_file = OutProcess(task_pers_df)
    workbook = out_file.get_task_xl()
    workbook.save(response)

    return response

# @login_required
# @user_passes_test(must_be_master)
def get_general_task_view(request, task_name):
    task_pers_df = read_frame(TaskPersonal.objects.filter(komax_task=get_object_or_404(KomaxTask, task_name=task_name)))

    task_pers_df.sort_values(
        by=['id'],
        ascending=True,
        inplace=True,
    )

    task_pers_df.drop(labels='worker', axis='columns', inplace=True)
    task_pers_df.index = pd.Index(range(task_pers_df.shape[0]))

    task_pers_df['done'] = ''

    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    )
    response['Content-Disposition'] = 'attachment; filename={task_name}.xlsx'.format(
        task_name=task_name,
    )

    out_file = OutProcess(task_pers_df)
    workbook = out_file.get_task_xl()
    ws = workbook.active
    workbook.save(response)

    return response

# @login_required
# @user_passes_test(must_be_master)
def get_personal_task_view_kappa(request, task_name, kappa):
    komax_task_obj = get_object_or_404(KomaxTask, task_name=task_name)

    kappa_task_pers_df = read_frame(TaskPersonal.objects.filter(komax_task=komax_task_obj, kappa=komax_task_obj.kappas))

    kappa_task_pers_df.sort_values(
        by=['id'],
        ascending=True,
        inplace=True,
    )
    kappa_task_pers_df.drop(labels='worker', axis='columns', inplace=True)
    kappa_task_pers_df.index = pd.Index(range(kappa_task_pers_df.shape[0]))

    kappa_task_pers_df['done'] = ''

    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    )
    response['Content-Disposition'] = 'attachment; filename={task_name}-{kappa_number}-Kappa.xlsx'.format(
        task_name=task_name,
        kappa_number=komax_task_obj.kappas.number,
    )

    out_file = OutProcess(kappa_task_pers_df)
    workbook = out_file.get_kappa_task_xl()
    workbook.save(response)

    return response

# @login_required
# @user_passes_test(must_be_master)
def get_komax_ticket_view(self, task_name, komax):
    komax_obj = get_object_or_404(Komax, number=komax)
    tasks_obj = get_object_or_404(KomaxTask, task_name=task_name)
    task_pers_df = read_frame(TaskPersonal.objects.filter(komax_task=tasks_obj, komax=komax_obj))

    task_pers_df.sort_values(
        by=['id'],
        ascending=True,
        inplace=True,
    )

    task_pers_df.index = pd.Index(range(task_pers_df.shape[0]))

    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    )
    response['Content-Disposition'] = 'attachment; filename={komax_number}-ticket.xlsx'.format(
        komax_number=komax,
    )

    out_file = OutProcess(task_pers_df)
    wb = out_file.get_labels()

    wb.save(response)
    return response

# @login_required
# @user_passes_test(must_be_master)
def get_kappa_ticket_view(request, task_name, kappa):
    task_obj = get_object_or_404(KomaxTask, task_name=task_name)
    task_pers_df = read_frame(TaskPersonal.objects.filter(komax_task=task_obj, kappa=task_obj.kappas))

    task_pers_df.sort_values(
        by=['id'],
        ascending=True,
        inplace=True,
    )

    task_pers_df.index = pd.Index(range(task_pers_df.shape[0]))

    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    )
    response['Content-Disposition'] = 'attachment; filename={kappa_number}-ticket.xlsx'.format(
        kappa_number=task_obj.kappas.number,
    )

    out_file = OutProcess(task_pers_df)
    wb = out_file.get_labels()

    wb.save(response)
    return response

