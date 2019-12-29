# All things with forms checkers

from .modules.HarnessProcessing import HarnessNumber
from .modules.HarnessChartProcessing import KomaxAppTaskName
from .models import Harness, KomaxTask, Komax
from django.db import close_old_connections
from channels.db import database_sync_to_async

class FieldChecker:

    def __init__(self):
        return

    def get_harnesses(self, harness_number):
        return Harness.objects.filter(harness_number=harness_number)

    def get_komaxes(self, komax):
        return Komax.objects.filter(number=komax)

    def get_task(self, task_name):
        return KomaxTask.objects.filter(task_name=task_name)

    async def field_check_harness_number(self, harness_number):
        harness_query = await database_sync_to_async(self.get_harnesses)(harness_number)
        if len(harness_query):
            return False
        else:
            number = HarnessNumber(harness_number)
            return number.check_harness_number()

    async def field_check_task_name(self, task_name):
        komax_task_query = await database_sync_to_async(self.get_task)(task_name)
        if len(komax_task_query):
            return False
        else:
            task = KomaxAppTaskName(task_name)
            return task.check_task_name()

    async def field_check_komax_number(self, komax):
        komax_query = await database_sync_to_async(self.get_komaxes)(komax)
        if len(komax_query):
            return False
        else:
            return True