from .checker import FieldChecker
from channels.generic.websocket import WebsocketConsumer
import json
import asyncio
from django.contrib.auth import get_user_model
from channels.consumer import AsyncConsumer
from channels.db import database_sync_to_async
from .modules.KomaxTaskProcessing import KomaxTaskProcessing, delete_komax_order, get_task_to_load
from .views import seconds_to_str_hours
from .models import KomaxTask, EmailUser, TaskPersonal, KomaxOrder, Komax
from django.db import close_old_connections
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from .task import send_mail_delay
from django.utils import translation
from django.utils.translation import gettext_lazy as _
from django_pandas.io import read_frame
import time
from django_pandas.io import read_frame
import pandas as pd

komax_status_dict = {komax.number: 0 for komax in Komax.objects.all()}
komax_task_df = None
task_pers_objs = TaskPersonal.objects.filter(komax_task__status__exact=3)
if task_pers_objs is not None:
    komax_task_df = read_frame(task_pers_objs)
    komax_task_df.index = pd.Index(komax_task_df['id'])

#komax_task_df.to_excel('New_excel.xlsx')

class KomaxAppTaskConsumer(AsyncConsumer):
    data_task = None
    data_alloc = None

    async def websocket_connect(self, event):
        # print("connected", event)
        await self.send({
            "type": "websocket.accept"
        })

    async def async_create_task(self, komax_task_name, harnesses, komaxes, kappas, shift,
                                     type_of_allocation='parallel'):
        """

        :param komax_task_name:
        :param harnesses:
        :param komaxes:
        :param shift:
        :param type_of_allocation: str, parallel or consistently
        :return:
        """
        """
        processor = KomaxTaskProcessing()
        await database_sync_to_async(processor.create_task)(
            komax_task_name,
            harnesses,
            komaxes,
            kappas,
            shift,
            type_of_allocation
        )
        """
        """
        self.data_task = await database_sync_to_async(self.create_sort_task)(
            komax_task_name,
            harnesses,
            komaxes,
            kappas,
            shift,
            type_of_allocation
        )
        """
    def create_sort_task(self, komax_task_name, harnesses, komaxes, kappas, shift, type_of_allocation='parallel'):
        """

        :param komax_task_name:
        :param harnesses:
        :param komaxes:
        :param shift:
        :param type_of_allocation: str, parallel or consistently
        :return:
        """
        processor = KomaxTaskProcessing()
        # return processor.create_task(komax_task_name, harnesses, komaxes, kappas, shift, type_of_allocation)
        # final_data = processor.sort_komax_task(komax_task_name)

        # return final_data

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

    def send_new_task_email(self, info_dict: dict):

        if type(info_dict['task_name']) is str and 'German' in info_dict['task_name']:
            return

        context = {
            'task_name': info_dict['task_name'],
        }

        email_html_path = 'komax_app/email_new_task_template.html'
        text = 'Task and allocation for {} created'.format(info_dict['task_name'])
        topic = 'Task and allocation created'
        from_send = settings.EMAIL_HOST_USER
        email_users = EmailUser.objects.all()
        to_send = [email_user.email for email_user in email_users]
        lang = translation.get_language()
        task = send_mail_delay.delay(email_html_path, context, from_send, to_send, _(topic), text, lang)

        return task

    def create_allocation(self, loaded_dict_data):
        processor = KomaxTaskProcessing()
        harness_amount_dict = loaded_dict_data

       #  processor.update_harness_amount(harness_amount_dict['task_name'], harness_amount_dict)

        data_alloc = processor.create_allocation(harness_amount_dict['task_name'])

        self.send_new_task_email(harness_amount_dict)

        return data_alloc

    def prepare_komax_task(self, komax_task_name, harnesses, komaxes, kappas, shift, type_of_allocation='parallel',
                           loading_type='New'):
        komax_task_processor = KomaxTaskProcessing()
        delete_komax_order()
        komax_task_processor.create_komax_task(komax_task_name, harnesses, komaxes, kappas, shift, type_of_allocation,
                                               loading_type)
        komax_task_processor.sort_save_komax_task(komax_task_name)

    def complete_komax_task(self, amount_info_dict):
        komax_task_processor = KomaxTaskProcessing()
        komax_task_name = amount_info_dict['task_name']
        harness_amount_dict = amount_info_dict['harness_amount']
        komax_task_processor.update_harness_amount(komax_task_name, harness_amount_dict)
        allocation = komax_task_processor.create_allocation(komax_task_name)
        komax_task_processor.update_komax_time(komax_task_name, {komax: time[0] for komax, time in allocation.items()})

    async def async_complete_komax_task(self, amount_info_dict):
        await database_sync_to_async(self.complete_komax_task)(amount_info_dict)

    async def async_prepare_komax_task(self, komax_task_name, harnesses, komaxes, kappas, shift,
                                 type_of_allocation='parallel', loading_type='New'):
        await database_sync_to_async(self.prepare_komax_task)(
            komax_task_name,
            harnesses,
            komaxes,
            kappas,
            shift,
            type_of_allocation,
            loading_type,
        )

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
                kappas = loaded_dict_data.get('kappas')
                shift = loaded_dict_data.get('shift')
                type_of_allocation = loaded_dict_data.get('type_of_allocation')
                loading_type = loaded_dict_data.get('loading_type')
                """
                if not result_good:
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
                """

                await self.async_prepare_komax_task(task_name, harnesses, komaxes, kappas, shift, type_of_allocation,
                                                    loading_type)

                final_data = {
                    'info_type': 'task_status',
                    'status': 'loaded',
                }
                await self.send({
                    "type": "websocket.send",
                    "text": json.dumps(final_data),
                })

            if loaded_dict_data['info_type'] == 'amount_info':
                task_name = loaded_dict_data['task_name']

                await self.async_complete_komax_task(loaded_dict_data)

                if self.data_alloc is not None and self.data_alloc == -1:
                    url = 'tasks/setup/'
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
                else:
                    url = '/tasks/' + task_name + '/'
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

    def __init__(self, scope):
        AsyncConsumer.__init__(self, scope)
        self.komax_number = 0

    async def websocket_connect(self, event):
        await self.send({
            "type": "websocket.accept"
        })

    def save_komax_task_personal(self, komax_number, komax_task_personal_df_dict):
        komax_task_processor = KomaxTaskProcessing()
        komax_task_processor.create_task_personal_from_dataframe_dict(komax_task_personal_df_dict)
        komax_task_processor.change_komax_order_status('Received', komax_number)

    async def async_save_komax_task_personal(self, komax_number, komax_task_personal_df_dict):
        await database_sync_to_async(self.save_komax_task_personal)(komax_number, komax_task_personal_df_dict)

    def get_komax_order(self, komax_number):
        komax_obj = Komax.objects.filter(number=komax_number)[0]
        komax_order_objs = KomaxOrder.objects.filter(komax=komax_obj)
        if len(komax_order_objs):
            return komax_order_objs[0]

        return None

    async def async_get_komax_order(self, komax_number):
        return await database_sync_to_async(self.get_komax_order)(komax_number)

    def get_new_komax_task_to_load(self, komax_number):
        return get_task_to_load(komax_number)

    async def async_get_new_komax_task_to_load(self, komax_number):
        return await database_sync_to_async(self.get_new_komax_task_to_load)(komax_number)

    def clean_komax_orders(self):
        delete_komax_order()

    async def async_delete_komax_orders(self):
        self.clean_komax_orders()

    def set_komax_task_df(self):
        global komax_task_df
        komax_task_df = read_frame(TaskPersonal.objects.filter(komax_task__status__exact=3))
        komax_task_df.index = pd.Index(komax_task_df['id'])

    async def async_set_komax_task_df(self):
        return await database_sync_to_async(self.set_komax_task_df)()

    async def websocket_receive(self, event):
        global komax_status_dict
        if 'text' in event:
            msg = json.loads(event['text'])
            if msg['status'] == 1:
                self.komax_number = msg['komax_number']
                komax_status_dict[msg['komax_number']] = msg['position']
                komax_order = await self.async_get_komax_order(msg['komax_number'])
                if komax_order is not None:
                    if komax_order.status == 'Requested':
                        dict_to_send = {
                            'status': 2,
                            'text': komax_order.status,
                        }
                        await self.send({
                            "type": "websocket.send",
                            "text": json.dumps(dict_to_send)
                        })
                    elif komax_order.status == 'Received':
                        komax_number = msg['komax_number']
                        new_komax_task_df = await self.async_get_new_komax_task_to_load(komax_number)
                        if new_komax_task_df is not None:
                            await self.async_set_komax_task_df()
                            dict_to_send = {
                                'status': 2,
                                'task': new_komax_task_df.to_dict()
                            }

                            await self.send({
                                "type": "websocket.send",
                                "text": json.dumps(dict_to_send)
                            })
                """
                elif True:
                    task_personal_df = await self.async_get_komax_task_dataframe(new_task)

                    dict_to_send = {
                        'status': 2,
                        'type': new_task.loaded,
                        'task': task_personal_df,
                    }
                    
                    
                    await self.send({
                        "type": "websocket.send",
                        "text": json.dumps(dict_to_send),
                    })
                
                await self.send({
                    "type": "websocket.send",
                    "text": json.dumps(event["text"]),
                })
                """
            elif msg['status'] == 2:
                if msg['text'] == 'Requested' and 'task' in msg:
                    komax_task_df_dict = msg['task']
                    komax_number = msg['komax_number']

                    await self.async_save_komax_task_personal(komax_number, komax_task_df_dict)


                """
                await self.send({
                    "type": "websocket.send",
                    "text": json.dumps(event["text"]),
                })
                """

            """
            else:
                await self.send({
                    "type": "websocket.send",
                    "text": json.dumps(event["text"]),
                })
            """
            """
            else:
                await self.send({
                    "type": "websocket.send",
                    "text": json.dumps(event["text"]),
                })
            """

    async def websocket_disconnect(self, event):
        global komax_status_dict
        komax_status_dict[self.komax_number] = 0
        await self.async_delete_komax_orders()
        return

class KomaxWebConsumer(AsyncConsumer):

    def __init__(self, scope):
        AsyncConsumer.__init__(self, scope)
        self.last_dict = None

    async def websocket_connect(self, event):
        await self.send({
            "type": "websocket.accept"
        })

    async def websocket_receive(self, event):
        global komax_status_dict

        while self.last_dict == komax_status_dict:
            await asyncio.sleep(1)
        else:
            komax_status_dict_tmp = dict()
            for komax, value in komax_status_dict.items():
                if type(value) is not int:
                    komax_status_dict_tmp[komax] = 2
                else:
                    komax_status_dict_tmp[komax] = value
            dict_to_send = {
                'komax_status_dict': komax_status_dict_tmp
            }
            await self.send({
                "type": "websocket.send",
                "text": json.dumps(dict_to_send)
            })

    async def websocket_disconnect(self, event):
        print("disconnect", event)

class WorkerConsumer(AsyncConsumer):

    def __init__(self, scope):
        AsyncConsumer.__init__(self, scope)
        self.last_dict = None

    async def websocket_connect(self, event):
        await self.send({
            "type": "websocket.accept",
        })

    # TODO: handle if True-all idx not found
    def get_harnesses_completion(self):
        global komax_task_df
        # print(komax_status_dict)
        komax_idx_dict = dict()
        for komax_number, position_dict in komax_status_dict.items():
            # print(komax_task_df)
            if position_dict != 1 and position_dict != 0:
            # print([i for i in komax_task_df.isin(position_dict).all(axis=1)])
            # print(komax_task_df[komax_task_df.isin(position_dict).all(axis=1)])
            # print(komax_task_df[komax_task_df.isin(position_dict).all(axis=1)].index.values)
            # idx = komax_task_df[komax_task_df.isin(position_dict).all(axis=1)].index.values[0]
                """print(komax_task_df)
                print(komax_task_df['id'])
                print(position_dict['id'])
                print(komax_task_df['id'] == position_dict['id'])
                print(komax_task_df[komax_task_df['id'] == position_dict['id']])"""
                idx = komax_task_df[komax_task_df['id'] == position_dict['id']].index.values[0]
                komax_idx_dict[komax_number] = idx


        harnesses = komax_task_df['harness'].unique()
        harness_time_dict = dict()
        for harness in harnesses:
            left_times = [
                sum(
                    komax_task_df[(komax_task_df['id'] >= idx) & (komax_task_df['harness'] == harness) & (komax_task_df['komax'] == str(komax))][
                        'time']) if idx is not None else 0 for komax, idx in komax_idx_dict.items()
            ]
            sum_all_times = [
                sum(komax_task_df[(komax_task_df['harness'] == harness) & (komax_task_df['komax'] == str(komax))][
                        'time']) if idx is not None else 0 for komax, idx in komax_idx_dict.items()
            ]

            if len(left_times) and len(sum_all_times):
                harness_time_dict[harness] = {
                    'left': seconds_to_str_hours(max(left_times)),
                    'all': round((sum(sum_all_times) - sum(left_times))/sum(sum_all_times)*100) if sum(sum_all_times) > 0 else 0,
                }
            else:
                harness_time_dict[harness] = {
                    'left': seconds_to_str_hours(0),
                    'all': 0,
                }

        print(harness_time_dict)
        return harness_time_dict

    async def async_get_harnesses_completion(self):
        return await database_sync_to_async(self.get_harnesses_completion)()

    def new_komax_status_dict(self):
        while self.last_dict == komax_status_dict:
            time.sleep(10)
        return True

    async def async_new_komax_status_dict(self):
        return await database_sync_to_async(self.new_komax_status_dict)()

    async def websocket_receive(self, event):
        global komax_status_dict
        global komax_task_df
        while self.last_dict == komax_status_dict:
            await asyncio.sleep(1)
        else:
            if komax_task_df is not None:

                # msg = json.loads(event['text'])
                self.last_dict = komax_status_dict

                data_to_send = await self.async_get_harnesses_completion()
                # print(data_to_send)
                await self.send({
                    "type": "websocket.send",
                    "text": json.dumps(data_to_send)
                })

    async def websocket_disconnect(self, event):
        return




