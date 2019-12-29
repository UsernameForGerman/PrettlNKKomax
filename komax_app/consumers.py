from .checker import FieldChecker
from channels.generic.websocket import WebsocketConsumer
import json
import asyncio
from django.contrib.auth import get_user_model
from channels.consumer import AsyncConsumer
from channels.db import database_sync_to_async
from .views import KomaxTaskProcessing
from .models import KomaxTask
from django.db import close_old_connections

class KomaxAppTaskConsumer(AsyncConsumer):
    data_task = None
    data_alloc = None

    async def websocket_connect(self, event):
        # print("connected", event)
        await self.send({
            "type": "websocket.accept"
        })

    async def async_create_sort_task(self, komax_task_name, harnesses, komaxes, shift):
        self.data_task = await database_sync_to_async(self.create_sort_task)(komax_task_name, harnesses, komaxes, shift)

    def create_sort_task(self, komax_task_name, harnesses, komaxes, shift):
        processor = KomaxTaskProcessing()
        processor.create_task(komax_task_name, harnesses, komaxes, shift)
        final_data = processor.sort_komax_task(komax_task_name)
        return final_data

    def delete_task(self, task_name):
        task = KomaxTask.objects.filter(task_name=task_name)
        if len(task):
            task = task[0]
            task.harnesses.clear()
            task.komaxes.clear()
            task.delete()

    async def async_delete_task(self, task_name):
        await database_sync_to_async(self.delete_task)(task_name)

    async def async_create_allocation(self, loaded_dict_data):
        self.data_alloc = await database_sync_to_async(self.create_allocation)(loaded_dict_data)

    def create_allocation(self, loaded_dict_data):
        processor = KomaxTaskProcessing()
        harness_amount_dict = loaded_dict_data

        processor.update_harness_amount(harness_amount_dict['task_name'], harness_amount_dict)

        self.data_alloc = processor.create_allocation(harness_amount_dict['task_name'])

    async def websocket_receive(self, event):
        # print("receive", event)

        front_text = event.get('text', None)
        if front_text is not None:
            loaded_dict_data = json.loads(front_text)

            if loaded_dict_data['info_type'] == 'checker_info':
                task_name = loaded_dict_data['task_name']
                checker = FieldChecker()
                data_to_send = {
                    'info_type': 'checker_info'
                }

                if await checker.field_check_task_name(task_name):
                    data_to_send['checker'] = 1
                else:
                    data_to_send['checker'] = 0

                await self.send({
                    "type": "websocket.send",
                    "text": json.dumps(data_to_send)
                })

            if loaded_dict_data['info_type'] == 'task_info':
                processor = KomaxTaskProcessing()
                task_name = loaded_dict_data.get('task_name')
                harnesses = loaded_dict_data.get('harnesses')
                komaxes = loaded_dict_data.get('komaxes')
                shift = loaded_dict_data.get('shift')

                await self.async_create_sort_task(task_name, harnesses, komaxes, shift)

                if self.data_task is not None and self.data_task['allocation'][0] == -1:
                    await self.async_delete_task(task_name)
                    url = '/komax_app/setup/'
                    response = {
                        "info_type": "page_status",
                        "status": "http_redirect",
                        "url": url,
                        "error": True,
                    }
                    await self.send({
                        "type": "websocket.send",
                        "text": json.dumps(response)
                    })

                final_data = {
                    'info_type': 'sort_data',
                    'allocation': self.data_task['allocation']
                }
                await self.send({
                    "type": "websocket.send",
                    "text": json.dumps(final_data),
                })

            if loaded_dict_data['info_type'] == 'amount_info':
                task_name = loaded_dict_data['task_name']

                await self.async_create_allocation(loaded_dict_data)

                if self.data_alloc is not None and self.data_alloc == -1:
                    url = '/komax_app/setup/'
                    response = {
                        "info_type": "page_status",
                        "status": "http_redirect",
                        "url": url,
                        "error": True
                    }
                    await self.send({
                        "type": "websocket.send",
                        "text": json.dumps(response)
                    })

                url = '/komax_app/task/' + task_name + '/'
                response = {
                    "info_type": "page_status",
                    "status": "http_redirect",
                    "url": url,
                }

                await self.send({
                    "type": "websocket.send",
                    "text": json.dumps(response)
                })


    async def websocket_disconnect(self, event):
        # print("disconnected", event)
        return

class HarnessConsumer(AsyncConsumer):
    async def websocket_connect(self, event):
        await self.send({
            "type": "websocket.accept"
        })

    async def websocket_receive(self, event):
        front_text = event.get('text', None)
        if front_text is not None:
            received_data = json.loads(front_text)
            harness_number = received_data.get('harness_number', None)
            if harness_number is not None:
                checker = FieldChecker()
                data_to_send = {}
                if await checker.field_check_harness_number(harness_number):
                    data_to_send['checker'] = 1
                else:
                    data_to_send['checker'] = 0

                await self.send({
                    "type": "websocket.send",
                    "text": json.dumps(data_to_send)
                })

    async def websocket_disconnect(self, event):
        return

class KomaxConsumer(AsyncConsumer):
    async def websocket_connect(self, event):
        await self.send({
            "type": "websocket.accept"
        })

    async def websocket_receive(self, event):
        front_text = event.get('text', None)
        if front_text is not None:
            received_data = json.loads(front_text)
            komax = received_data.get('komax', None)
            if komax is not None:
                checker = FieldChecker()
                data_to_send = {}
                if await checker.field_check_komax_number(komax):
                    data_to_send['checker'] = 1
                else:
                    data_to_send['checker'] = 0

                await self.send({
                    "type": "websocket.send",
                    "text": json.dumps(data_to_send)
                })

    async def websocket_disconnect(self, event):
        return



