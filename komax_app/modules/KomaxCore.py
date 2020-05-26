from komax_app.models import KomaxStatus, TaskPersonal, Komax, KomaxOrder
from .KomaxTaskProcessing import KomaxTaskProcessing


def create_update_komax_status( komax_number, position_info):
    komax_status_query = KomaxStatus.objects.filter(komax__number__exact=komax_number)
    if len(komax_status_query):
        komax_status_obj = komax_status_query.first()
        if type(position_info) is dict:
            komax_status_obj.task_personal = TaskPersonal.objects.filter(id=int(position_info['id'])).first()
        elif type(position_info) is int:
            komax_status_obj.task_personal = None
        komax_status_obj.save(update_fields=['task_personal'])
    else:
        komax_obj = Komax.objects.filter(number=komax_number)
        task_personal = None
        if type(position_info) is dict:
            task_personal = TaskPersonal.objects.filter(id=int(position_info['id']))
            if len(task_personal):
                task_personal = task_personal[0]
        elif type(position_info) is int:
            task_personal = None
        if len(komax_obj):
            KomaxStatus(komax=komax_obj.first(), task_personal=task_personal).save()
        else:
            pass

def get_komax_order(komax_number):
    komax_obj = Komax.objects.filter(number=komax_number)[0]
    komax_order_objs = KomaxOrder.objects.filter(komax=komax_obj)
    if len(komax_order_objs):
        return komax_order_objs[0]

    return None

def save_komax_task_personal(komax_number, komax_task_personal_df_dict, worker):
    komax_task_processor = KomaxTaskProcessing()
    komax_task_processor.create_task_personal_from_dataframe_dict(komax_task_personal_df_dict, worker, komax_number)
    komax_task_processor.delete_komax_order(komax_number)

def delete_komax_status(komax_number):
    KomaxStatus.objects.filter(komax__number__exact=komax_number).delete()


