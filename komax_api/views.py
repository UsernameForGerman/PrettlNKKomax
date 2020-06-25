# django libs
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_201_CREATED, \
    HTTP_500_INTERNAL_SERVER_ERROR, HTTP_204_NO_CONTENT
from django.shortcuts import get_object_or_404

# project libs
from .permissions import KomaxIsAuthenticated
from komax_app.models import Komax, Worker
from komax_app.modules.KomaxCore import create_update_komax_status, get_komax_order, delete_komax_status, \
    save_komax_task_personal
from komax_app.modules.KomaxTaskProcessing import get_task_to_load, delete_komax_order

# others
from json import loads

class KomaxClientAPIView(APIView):
    permission_classes = (KomaxIsAuthenticated, )

    def get_komax_number(self):
        return get_object_or_404(Komax, identifier=self.request.session.get('komax-id')).number

    def get_worker(self, komax_number):
        return get_object_or_404(Worker, komax=komax_number)

class PositionInfoView(KomaxClientAPIView):

    def post(self, *args, **kwargs):
        komax_number = self.get_komax_number()
        position_info = self.request.POST['position'] if 'position' in self.request.POST else None
        if position_info is not None:
            create_update_komax_status(komax_number, position_info)
            return Response(status=HTTP_201_CREATED)
        return Response(status=HTTP_400_BAD_REQUEST)

class KomaxTaskPersonalView(KomaxClientAPIView):

    def get(self, *args, **kwargs):
        komax_number = self.get_komax_number()
        komax_order = get_komax_order(komax_number)
        if komax_order is None:
            return Response('New tasks not found', status=HTTP_204_NO_CONTENT)

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

        return Response(data=params, status=HTTP_200_OK)

    def put(self, *args, **kwargs):
        task_json = self.request.POST['task'] if 'task' in self.request.POST else None
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

    def delete(self, *args, **kwargs):
        komax_number = self.get_komax_number()
        delete_komax_status(komax_number)
        delete_komax_order()
        del self.request.session['komax-id']
        return Response('Deleted successfully. Goodbuy.', status=HTTP_200_OK)
