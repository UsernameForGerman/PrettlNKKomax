import json

import channels.layers
from asgiref.sync import async_to_sync

from django.db.models import Sum
from django.db.models.signals import post_save, pre_delete, pre_save
from django.dispatch import receiver
from django_pandas.io import read_frame

from collections import Counter
from . import models

changes_d = dict()
idxs = list()


# def send_message(event):
#     '''
#     Call back function to send message to the browser
#     '''
#     message = event['text']
#     channel_layer = channels.layers.get_channel_layer()
#     # Send message to WebSocket
#     async_to_sync(channel_layer.send)(text_data=json.dumps(
#         message
#     ))
#
# @receiver(pre_save, sender=models.KomaxStatus)
# def update_komax_status_listeners(sender, instance, **kwargs):
#     global idxs
#     '''
#     Sends KomaxStatus status to the browser when KomaxStatus updated
#     '''
#     if kwargs.get('created', True):
#         """
#         To komax statuses send
#         """
#         group_name = 'komax-status'
#
#         message = {
#             'komax': instance.komax.number,
#             'status': 2 if instance.task_personal is not None else 1,
#         }
#
#         channel_layer = channels.layers.get_channel_layer()
#
#         async_to_sync(channel_layer.group_send)(
#             group_name,
#             {
#                 'type': 'send_message',
#                 'text': message
#             }
#         )
#
#         """
#         To Worker account harness completion send
#         """
#         group_name = 'worker-account'
#
#         for msg in msg_new_komax_status_harness_completion(instance):
#             channel_layer = channels.layers.get_channel_layer()
#             # print(msg)
#             async_to_sync(channel_layer.group_send)(
#                 group_name,
#                 {
#                     'type': 'send_message',
#                     'text': msg
#                 }
#             )
#
# def msg_new_komax_status_harness_completion(instance):
#     komax_task_df = read_frame(models.TaskPersonal.objects.filter(komax_task__status__exact=3))
#     komax_idx_dict = dict()
#     for komax in models.Komax.objects.all():
#         komax_idx_dict[komax.number] = 0
#         if instance.komax == komax:
#             if instance.task_personal is not None:
#                 komax_idx_dict[instance.komax.number] = instance.task_personal_id
#         else:
#             try:
#                 komax_status = models.KomaxStatus.objects.get(komax=komax)
#                 if komax_status.task_personal is not None:
#                     komax_idx_dict[komax.number] = komax_status.task_personal_id
#             except models.KomaxStatus.DoesNotExist:
#                 pass
#
#     harnesses = komax_task_df['harness'].unique()
#     for harness in harnesses:
#         left_times = [
#             sum(
#                 komax_task_df[(komax_task_df['id'] > idx) & (komax_task_df['harness'] == harness) & (
#                         komax_task_df['komax'] == str(komax))][
#                     'time']) if idx is not None else 0 for komax, idx in komax_idx_dict.items()
#         ]
#         sum_all_times = [
#             sum(komax_task_df[
#                     (komax_task_df['harness'] == harness) & (komax_task_df['komax'] == str(komax))][
#                     'time']) if idx is not None else 0 for komax, idx in komax_idx_dict.items()
#         ]
#
#         if len(left_times) and len(sum_all_times):
#
#
#             message = {
#                 'number': harness,
#                 'percent': round((1 - sum(left_times)/sum(sum_all_times)) * 100) if sum(sum_all_times) > 0 else 0,
#                 'left': max(left_times),
#                 'all': sum(sum_all_times) if sum(sum_all_times) > 0 else 0,
#             }
#         else:
#             message = {
#                 'number': harness,
#                 'percent': 0,
#                 'left': 0,
#                 'all': 0,
#             }
#
#         yield message
#
# @receiver(pre_delete, sender=models.KomaxStatus)
# def delete_komax_status_listeners(sender, instance, **kwargs):
#     message = {
#         'komax': instance.komax.number,
#         'status': 0,
#     }
#     group_name = 'komax-status'
#
#     channel_layer = channels.layers.get_channel_layer()
#
#     async_to_sync(channel_layer.group_send)(
#         group_name,
#         {
#             'type': 'send_message',
#             'text': message
#         }
#     )

