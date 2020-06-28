# django libs
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_201_CREATED, \
    HTTP_500_INTERNAL_SERVER_ERROR, HTTP_204_NO_CONTENT, HTTP_404_NOT_FOUND
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt

# project libs
from .permissions import KomaxIsAuthenticated
from komax_app.models import Komax, Worker
from komax_app.modules.KomaxCore import create_update_komax_status, get_komax_order, delete_komax_status, \
    save_komax_task_personal
from komax_app.modules.KomaxTaskProcessing import get_task_to_load, delete_komax_order

# others
from json import loads

class KomaxClientLoginView(APIView):
    authentication_classes = ()
    permission_classes = (AllowAny, )

    def post(self, *args, **kwargs):
        komax_id = self.request.data.get('Komax', None)
        if Komax.objects.in_bulk(['{}'.format(komax_id)], field_name='identifier'):
            self.request.session['komax-id'] = komax_id
            return Response(status=HTTP_200_OK)
        else:
            return Response(status=HTTP_404_NOT_FOUND)

class KomaxClientAPIView(APIView):
    permission_classes = (KomaxIsAuthenticated, )
    authentication_classes = ()

    def get_komax_number(self):
        return get_object_or_404(Komax, identifier=self.request.session.get('komax-id')).number

    def get_worker(self, komax_number):
        return get_object_or_404(Worker, current_komax=komax_number)

class PositionInfoView(KomaxClientAPIView):

    def post(self, *args, **kwargs):
        komax_number = self.get_komax_number()
        position_info = loads(self.request.data['position']) if 'position' in self.request.data else None
        if position_info is not None:
            create_update_komax_status(komax_number, position_info)
            return Response(status=HTTP_201_CREATED)
        return Response(status=HTTP_400_BAD_REQUEST)

class KomaxTaskPersonalView(KomaxClientAPIView):

    def get(self, *args, **kwargs):
        komax_number = self.get_komax_number()
        komax_order = get_komax_order(komax_number)
        if komax_order is None:
            return Response('New tasks not found', status=HTTP_404_NOT_FOUND)

        if komax_order.status == 'Requested':
            params = {
                'text': komax_order.status,
            }
        elif komax_order.status == 'Received':
            new_komax_task_df = get_task_to_load(komax_number)
            params = {
                'task': new_komax_task_df.to_dict(),
                'text': komax_order.status
            }
        else:
            return Response(status=HTTP_500_INTERNAL_SERVER_ERROR)
        print(params)
        return Response(data=params, status=HTTP_200_OK)

    def put(self, *args, **kwargs):
        task_json = self.request.data['task'] if 'task' in self.request.data else None
        print(task_json)
        if task_json is None:
            return Response('No task provided', status=HTTP_400_BAD_REQUEST)

        komax_number = self.get_komax_number()
        worker = self.get_worker(komax_number)
        try:
            task = loads(task_json)
        except Exception as e:
            print(e)
            return Response('Can\'t decode from json. Error: {}'.format(e), status=HTTP_500_INTERNAL_SERVER_ERROR)

        save_komax_task_personal(komax_number, task, worker)
        return Response('Updated task personal successfully', status=HTTP_200_OK)

class KomaxClientLogoutView(KomaxClientAPIView):

    def delete(self, *args, **kwargs):
        komax_number = self.get_komax_number()
        delete_komax_status(komax_number)
        delete_komax_order()
        del self.request.session['komax-id']
        return Response('Deleted successfully. Goodbuy.', status=HTTP_200_OK)
