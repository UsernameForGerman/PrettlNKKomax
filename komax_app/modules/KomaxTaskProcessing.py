from komax_app.models import Harness, HarnessChart, HarnessAmount, KomaxTime, KomaxTask, Komax, TaskPersonal,\
    Laboriousness, KomaxTerminal, Kappa, KomaxOrder, KomaxSeal
import pandas as pd
from django_pandas.io import read_frame
from .HarnessChartProcessing import ProcessDataframe, get_time_from
from channels.db import database_sync_to_async
import time
from django.shortcuts import get_object_or_404


def get_komax_task_status_on_komax(komax_task, komax_number):
    if TaskPersonal.objects.filter(komax__number=komax_number, worker=None, komax_task=komax_task, loaded=False):
        return 2  # не загружено
    elif TaskPersonal.objects.filter(komax__number=komax_number, worker=None, komax_task=komax_task, loaded=True):
        return 3  # загружено
    else:
        return 4  # сделано

def get_shift(komax_task_obj):
    return komax_task_obj.shift


def save_obj(obj):
    obj.save()


def get_komax_task(task_name):
    return KomaxTask.objects.filter(task_name=task_name)


def get_harnesses(komax_task_obj=None, harness=None):
    if komax_task_obj is None:
        if harness is None:
            return Harness.objects.all()
        else:
            return Harness.objects.filter(harness_number=harness)
    else:
        return komax_task_obj.harnesses.all()


def get_komaxes(komax_task_obj=None, komax=None):
    if komax_task_obj is None:
        if komax is None:
            return Komax.objects.all()
        else:
            return Komax.objects.filter(number=komax)
    else:
        return komax_task_obj.komaxes.all()


def get_harness_chart(harness_obj=None):
    if harness_obj is not None:
        return HarnessChart.objects.filter(harness=harness_obj)
    else:
        return HarnessChart.objects.all()


def get_task_personal(task_obj=None, output='object'):
    if task_obj is None:
        task_personal_obj = TaskPersonal.objects.all()
    else:
        task_personal_obj = TaskPersonal.objects.filter(komax_task=task_obj)

    if output == 'object':
        return task_personal_obj
    elif output == 'dataframe':
        if len(task_personal_obj):
            task_df = read_frame(task_personal_obj).sort_values(
                by=['id'],
                ascending=True,
            )
            task_df.index = pd.Index(range(task_df.shape[0]))
            return task_df
        else:
            return pd.DataFrame({})


def get_laboriousness():
    return Laboriousness.objects.all()


def get_kappas(kappa_number=1):
    if kappa_number is None:
        return [None, ]
    else:
        return Kappa.objects.filter(number=kappa_number)


def get_komax_terminals():
    return KomaxTerminal.objects.all()

def get_komax_seals():
    return KomaxSeal.objects.all()

def get_df_from_harnesses(harnesses):
    harness_charts = list()
    for harness in harnesses:
        harness_chart = get_harness_chart(harness_obj=harness.harness)
        harness_charts.append(harness_chart)

    dataframe = pd.concat(
        [read_frame(harness_chart) for harness_chart in harness_charts],
        ignore_index=True
    )

    return dataframe

def get_komax_dict_from_query(komax_query):
    return {komax.number: (komax.status, komax.marking, komax.pairing, komax.group_of_square) for komax in komax_query}

def delete_komax_order(komax_number=None):
    if komax_number is None:
        KomaxOrder.objects.all().delete()
    else:
        KomaxOrder.objects.filter(komax=Komax.objects.filter(number=komax_number)[0]).delete()

def get_task_to_load(komax_number):
    komax = get_komaxes(komax=komax_number)[0]
    task_pers_objs = TaskPersonal.objects.filter(loaded=True, komax=komax, worker__isnull=True)
    task_pers_df = read_frame(task_pers_objs)
    if len(task_pers_df):
        delete_komax_order(komax_number)
        # for task_pers_obj in task_pers_objs:
        #     task_pers_obj.loaded = False
        #     TaskPersonal.objects.bulk_update(task_pers_objs, ['loaded'])
        return task_pers_df

    return pd.DataFrame()

def stop_komax_task_on_komax(komax, komax_task):
    if TaskPersonal.objects.filter(komax=komax, loaded=True, komax_task=komax_task).exists():
        KomaxOrder.objects.create(komax_task=komax_task, komax=komax, status="Requested")
    else:
        pass

def update_komax_task_status(komax_task):
    task_perss = TaskPersonal.objects.filter(komax_task=komax_task)
    base_status = komax_task.status
    if not len(task_perss.filter(worker__isnull=True)):
        komax_task.status = 4
    elif not len(task_perss.filter(loaded=False)) or not len(task_perss.filter(loaded=False, worker__isnull=True)):
        komax_task.status = 3
    else:
        komax_task.status = 2
    # elif not len(task_perss.filter(loaded=True)):
    #     komax_task.status = 2
    # elif len(task_perss.exclude(loaded=True)) and not len(task_perss.filter(loaded=False, worker__isnull=False)):
    #     komax_task.status = 1

    print(komax_task.status)
    print(base_status)
    if komax_task.status != base_status:
        komax_task.save(update_fields=['status'])

class KomaxTaskProcessing():

    def __init__(self):
        return

    def get_params_from_komax_task(self, komax_task):
        harnesses = get_harnesses(komax_task_obj=komax_task)
        kappas = [komax_task.kappas]
        shift = get_shift(komax_task)
        komax_dict = get_komax_dict_from_query([komax_time.komax for komax_time in get_komaxes(komax_task_obj=komax_task)])
        type_of_allocation = komax_task.type_of_allocation
        task_name = komax_task.task_name

        return (harnesses, komax_dict, kappas, shift, type_of_allocation)

    def load_task_personal(self, komax_task_name, komax_num):
        komax_task_query = get_komax_task(komax_task_name) #Все комаксы_таск с нужным именем
        if len(komax_task_query):
            task_pers_objs = TaskPersonal.objects.filter(
                komax_task__task_name=komax_task_name,
                komax__number=komax_num
            ).exclude(
                worker__isnull=False
            )
            for task_pers_obj in task_pers_objs:
                task_pers_obj.loaded = True        #ТаскПерсонал ставится loaded=True
            TaskPersonal.objects.bulk_update(task_pers_objs, ['loaded'])
        else:
            return
    # TODO: increase speed of func
    def __create_harness_amount(self, harnesses, amount=-1):
        harness_amount_objs = list()
        for harness in harnesses:
            harness_amount_obj = HarnessAmount(harness=Harness.objects.filter(harness_number=harness)[0], amount=amount)
            harness_amount_objs.append(harness_amount_obj)
            save_obj(harness_amount_obj)

        return harness_amount_objs

    # TODO: increase speed of func
    def __create_komax_time(self, komaxes, time=0):
        komax_time_objs = list()
        for komax in komaxes:
            komax_time_obj = KomaxTime(komax=Komax.objects.filter(number=komax)[0], time=time)
            komax_time_objs.append(komax_time_obj)
            save_obj(komax_time_obj)

        return komax_time_objs

    def __create_komax_orders(self, komax_task_obj, komax_objs, status):
        komax_order_objs = [
            KomaxOrder(
                komax_task=komax_task_obj,
                komax=komax,
                status=status,
            )
            for komax in komax_objs
        ]
        KomaxOrder.objects.bulk_create(komax_order_objs)

    def create_komax_task(self, task_name, harnesses, komaxes, kappas, shift, type_of_allocation, loading_type):
        harness_amount_objs = self.__create_harness_amount(harnesses)
        komax_time_objs = self.__create_komax_time(komaxes)
        kappa_obj = None
        if len(kappas):
            kappas_query = get_kappas(kappas[0])
            if len(kappas_query):
                kappa_obj = kappas_query[0]
        komax_task_obj = KomaxTask(
            task_name=task_name,
            kappas=kappa_obj,
            shift=shift,
            type_of_allocation=type_of_allocation,
            loading_type=loading_type,
        )
        save_obj(komax_task_obj)
        komax_task_obj.harnesses.add(*harness_amount_objs)
        komax_task_obj.komaxes.add(*komax_time_objs)
        save_obj(komax_task_obj)

        if loading_type == 'Mix' or loading_type == 'Urgent':
            self.__create_komax_orders(komax_task_obj, [komax.komax for komax in komax_time_objs], 'Requested')
        # elif loading_type == 'New':
        #     self.__create_komax_orders(komax_task_obj, [komax.komax for komax in komax_time_objs], 'Received')

        return True

    #TODO: increase speed of func
    def update_harness_amount(self, komax_task_name, harness_amount_dict):
        komax_task_obj = get_komax_task(komax_task_name)[0]
        harnesses = get_harnesses(komax_task_obj)
        for harness in harnesses:
            harness.amount = harness_amount_dict[str(harness)]
            save_obj(harness)

        tasks_pers = get_task_personal(komax_task_obj)

        for task_pers in tasks_pers:
            for harness in harness_amount_dict:
                if str(task_pers.harness.harness_number) in harness['harness']:
                    task_pers.amount = harness['amount']
            if str(task_pers.harness.harness_number) in harness_amount_dict:
                task_pers.amount = harness_amount_dict[str(task_pers.harness.harness_number)]
                save_obj(task_pers)
            else:
                pass

    # TODO: increase speed of func
    def update_komax_time(self, komax_task_name, komax_time_dict):
        komax_task_obj = get_komax_task(komax_task_name)[0]
        komaxes = get_komaxes(komax_task_obj=komax_task_obj)
        for komax in komaxes:
            komax.time = int(komax_time_dict[komax.komax.number])
            save_obj(komax)

    def __save_task_personal_from_dataframe(self, dataframe, komax_task_obj):
        for row in dataframe.iterrows():
            row_dict = row[1]
            harness_obj = get_harnesses(harness=row_dict['harness'])[0]
            if 'komax' not in row_dict:
                row_dict['komax'] = None

            if row_dict['komax'] is None:
                komax_obj = None
            else:
                komax_obj = get_komaxes(komax=row_dict['komax'])[0]

            if 'kappa' not in row_dict:
                row_dict['kappa'] = None

            if row_dict['kappa'] is None:
                kappa_obj = None
            else:
                kappa_obj = get_kappas(kappa_number=row_dict['kappa'])[0]

            self.save_task_personal(row_dict, komax_task_obj, kappa_obj, harness_obj, komax_obj)

    def __left_filter_columns(self, left_df, right_df):
        columns_to_drop = list()
        for col in right_df.columns:
            if col not in left_df:
                columns_to_drop.append(col)
        right_df.drop(columns_to_drop, axis='columns', inplace=True)

        return right_df

    def sort_save_komax_task(self, task_name):
        """
        sort komax task
        :param task_name:
        :param type_of_allocation: str, parallel or consistently
        :return:
        """
        task_obj = get_komax_task(task_name)[0]
        harnesses, komax_dict, kappas, shift, type_of_allocation = self.get_params_from_komax_task(task_obj)
        harnesses_komax_df = get_df_from_harnesses(harnesses)
        received = False

        while not received:
            received = True
            komax_orders = KomaxOrder.objects.all()
            for komax_order in komax_orders:
                if komax_order.status == 'Requested':
                    received = False
            time.sleep(1)

        base_komax_df = None
        if task_obj.loading_type == 'Mix':
            base_komax_df = get_task_personal(task_obj, output='dataframe')
            komax_df = self.__left_filter_columns(harnesses_komax_df, base_komax_df.copy())
            harnesses_komax_df = pd.concat([harnesses_komax_df, komax_df], ignore_index=True)

        time_dict = get_time_from(read_frame(get_laboriousness()))
        terminals = get_komax_terminals()
        seals = get_komax_seals()

        dataframe = self.__sort_task(
            harnesses_komax_df,
            terminals,
            seals,
            time_dict,
        )

        if base_komax_df is not None:

            for idx, row in dataframe.iterrows():
                for idx_2, row_2 in base_komax_df.iterrows():
                    if dataframe.loc[idx, 'id'] == base_komax_df.loc[idx_2, 'id']:
                        dataframe.loc[idx, 'amount'] = base_komax_df.loc[idx_2, 'amount']

        """
        if final_data['allocation'][0] == -1:
            task_obj.harnesses.all().delete()
            task_obj.komaxes.all().delete()
            task_obj.delete()
            return final_data
        """

        """
        process = ProcessDataframe(df)
        alloc_base = process.task_allocation_base(komax_dict, amount_dict, time_dict, hours=shift)

        process.delete_word_contain('СВ', 'R')
        first_sort = process.chart.nunique()["wire_terminal_1"] <= process.chart.nunique()["wire_terminal_2"]
        process.sort(method='simple', first_sort=first_sort)
        alloc = process.task_allocation(komax_dict, amount_dict, time_dict, hours=shift)

        first_sort = not first_sort
        new_process = ProcessDataframe(df)
        new_process.sort(method='simple', first_sort=first_sort)
        new_alloc = new_process.task_allocation(komax_dict, amount_dict, time_dict, hours=shift)

        if new_alloc == -1 and alloc == -1:
            task_obj.delete()
            return render(request, 'komax_app/task_status.html')
        elif new_alloc == -1:
            final_alloc = alloc
            final_chart = process.chart
        elif alloc == -1:
            final_alloc = new_alloc
            final_chart = new_process.chart
        else:
            sum_first = sum([i[0] for i in alloc.values()])
            sum_new = sum([i[0] for i in new_alloc.values()])

            if sum_new < sum_first:
                final_chart = new_process.chart
                final_alloc = new_alloc
            else:
                final_chart = process.chart
                final_alloc = alloc

        final_chart.drop(
            columns=['tube_len_2', 'tube_len_1', 'armirovka_2', 'armirovka_1', 'id'],
            inplace=True
        )

        for row in final_chart.iterrows():
            row_dict = row[1]
            task_pers_obj = TaskPersonal(
                task=task_obj,
                harness=get_object_or_404(Harness, harness_number=row_dict['harness']),
                komax=get_object_or_404(Komax, number=row_dict['komax']),
                amount=row_dict["amount"],
                notes=row_dict["notes"],
                marking=row_dict["marking"],
                wire_type=row_dict["wire_type"],
                wire_number=row_dict["wire_number"],
                wire_square=float(row_dict["wire_square"]),
                wire_color=row_dict["wire_color"],
                wire_length=int(row_dict["wire_length"]),
                wire_seal_1=row_dict["wire_seal_1"],
                wire_cut_length_1=float(row_dict["wire_cut_length_1"]),
                wire_terminal_1=row_dict["wire_terminal_1"],
                aplicator_1=row_dict["aplicator_1"],
                wire_seal_2=row_dict["wire_seal_2"],
                wire_cut_length_2=float(row_dict["wire_cut_length_2"]),
                wire_terminal_2=row_dict["wire_terminal_2"],
                aplicator_2=row_dict["aplicator_2"],
            )
            task_pers_obj.save()

        for komax, time in final_alloc.items():
            KomaxTaskAllocation(task=task_obj, komax=get_object_or_404(Komax, number=komax), time=time[0]).save()

        for key, item in final_alloc.items():
            hours = round(final_alloc[key][0] // 3600)
            final_alloc[key] = str(hours) + ':' + str(round((final_alloc[key][0] / 3600 - hours) * 60))

        for key, item in alloc_base.items():
            hours = round(alloc_base[key][0] // 3600)
            alloc_base[key] = str(hours) + ':' + str(round((alloc_base[key][0] / 3600 - hours) * 60))

        for key, item in final_alloc.items():
            final_alloc[key] = [final_alloc[key], alloc_base[key]]
        """

        self.__create_task_personal_from_dataframe(dataframe, task_obj)
        return

    def save_task_personal(self, row_dict, task_obj, kappa_obj, harness_obj, komax_obj):
        task_pers_obj = TaskPersonal(
            komax_task=task_obj,
            # harness=get_object_or_404(Harness, harness_number=row_dict['harness']),
            # komax=get_object_or_404(Komax, number=row_dict['komax']),
            harness=harness_obj,
            komax=komax_obj,
            kappa=kappa_obj,
            amount=int(row_dict["amount"]),
            notes=str(row_dict["notes"]),
            marking=str(row_dict["marking"]),
            wire_type=str(row_dict["wire_type"]),
            wire_number=str(row_dict["wire_number"]),
            wire_square=float(row_dict["wire_square"]),
            wire_color=str(row_dict["wire_color"]),
            wire_length=int(row_dict["wire_length"]),
            tube_len_1=str(row_dict["tube_len_1"]),
            wire_seal_1=str(row_dict["wire_seal_1"]),
            wire_cut_length_1=float(row_dict["wire_cut_length_1"]),
            wire_terminal_1=str(row_dict["wire_terminal_1"]),
            aplicator_1=str(row_dict["aplicator_1"]),
            tube_len_2=str(row_dict["tube_len_2"]),
            wire_seal_2=str(row_dict["wire_seal_2"]),
            wire_cut_length_2=float(row_dict["wire_cut_length_2"]),
            wire_terminal_2=str(row_dict["wire_terminal_2"]),
            aplicator_2=str(row_dict["aplicator_2"]),
            # time=row_dict['time']
        )
        task_pers_obj.save()

    def __sort_task(self, df, terminals, seals, time_dict):

        process = ProcessDataframe(df)
        process.filter_availability_komax_terminal_seal(terminals, seals)
        process.make_best_sort(quantity=1, time=time_dict)
        return process.chart

        """
        amount_dict = {harness.harness.harness_number: 1 for harness in harnesses}

        # alloc_base = process.task_allocation_base(komax_dict, amount_dict, time_dict, hours=shift)
        alloc_base = process.allocate(komax_dict, kappas, amount_dict, time_dict, shift, type_of_allocation=type_of_allocaton)

        process.delete_word_contain('СВ', 'R')
        first_sort = process.chart.nunique()["wire_terminal_1"] <= process.chart.nunique()["wire_terminal_2"]
        process.sort(method='simple', first_sort=first_sort)

        # alloc = process.task_allocation(komax_dict, amount_dict, time_dict, hours=shift)
        alloc = process.allocate(komax_dict, kappas, amount_dict, time_dict, shift, type_of_allocation=type_of_allocaton)

        first_sort = not first_sort
        new_process = ProcessDataframe(df)
        new_process.sort(method='simple', first_sort=first_sort)

        # new_alloc = new_process.task_allocation(komax_dict, amount_dict, time_dict, hours=shift)
        new_alloc = new_process.allocate(komax_dict, kappas, amount_dict, time_dict, shift, type_of_allocation=type_of_allocaton)

        if new_alloc == -1 and alloc == -1:
            final_data = {
                'allocation': [-1, alloc_base],
                'chart': -1
            }
        elif new_alloc == -1:
            final_data = {
                'allocation': [alloc, alloc_base],
                'chart': process.chart
            }
        elif alloc == -1:
            final_data = {
                'allocation': [new_alloc, alloc_base],
                'chart': new_process.new_chart
            }
        else:
            sum_first = sum([i[0] for i in alloc.values()])
            sum_new = sum([i[0] for i in new_alloc.values()])

            if sum_new < sum_first:
                final_data = {
                    'allocation': [new_alloc, alloc_base],
                    'chart': new_process.chart,
                }
            else:
                final_data = {
                    'allocation': [alloc, alloc_base],
                    'chart': process.chart,
                }
                
        return final_data
        """

    def __get_amount_dict(self, task_name):
        komax_task_query = get_komax_task(task_name)
        komax_task = komax_task_query[0]
        komax_task_harnesses = get_harnesses(komax_task_obj=komax_task)
        return {harness.harness.harness_number: harness.amount for harness in komax_task_harnesses}

    def __update_task_personal_from_dataframe(self, dataframe, komax_task_obj):
        komaxes_objs = get_komaxes()
        kappas_objs = get_kappas()
        komaxes = {komax.number: komax for komax in komaxes_objs}
        kappas = {kappa.number: kappa for kappa in kappas_objs}
        task_pers_objs = get_task_personal(task_obj=komax_task_obj)
        for task_pers in task_pers_objs:
            dataframe_position = dataframe[dataframe['id'] == task_pers.id]
            komax_number = dataframe_position['komax'].iloc[0]
            kappa_number = dataframe_position['kappa'].iloc[0]

            task_pers.komax = komaxes[komax_number] if komax_number is not None else None
            task_pers.kappa = kappas[kappa_number] if kappa_number is not None else None
            task_pers.time = dataframe_position['time'].iloc[0]
        TaskPersonal.objects.bulk_update(task_pers_objs, ['komax', 'kappa', 'time'])

    #TODO: if harness obj not excisted, but it is in df, return smthg
    def __create_task_personal_from_dataframe(self, dataframe, komax_task_obj, worker=None, komax_number=None, harnesses_number=None):



        if dataframe.empty and worker is not None:
            tasks_pers = TaskPersonal.objects.filter(komax__number=komax_number)
            for task in tasks_pers:
                task.loaded = False
            TaskPersonal.objects.bulk_update(tasks_pers, ['loaded'])

            if worker is not None:
                for task in tasks_pers:
                    task.worker = worker
                TaskPersonal.objects.bulk_update(tasks_pers, ['worker'])
                update_komax_task_status(komax_task_obj)
        else:
            if worker is not None:
                tasks_pers = TaskPersonal.objects.filter(komax__number=komax_number)
                for task in tasks_pers:
                    task.loaded = False
                TaskPersonal.objects.bulk_update(tasks_pers, ['loaded'])
                wire_number = [str(wire_number) for wire_number in dataframe.loc[:, 'wire_number']]
                # Stop
                if worker is not None:
                    finished_tasks = tasks_pers.exclude(wire_number__in=wire_number)
                    for task in finished_tasks:
                        task.worker = worker
                    TaskPersonal.objects.bulk_update(finished_tasks, ['worker'])
                    # update curr komax task status
                    update_komax_task_status(tasks_pers.first().komax_task)
                if tasks_pers.first().komax_task.task_name != komax_task_obj.task_name:
                    # update last komax task status
                    update_komax_task_status(tasks_pers.first().komax_task)
                    # Mix type of loading
                    not_finished_tasks = tasks_pers.filter(wire_number__in=wire_number)
                    for task in not_finished_tasks:
                        task.id = None
                        task.komax_task = komax_task_obj
                        task.komax = None
                        task.kappa = None
                        task.amount = 1
                    TaskPersonal.objects.bulk_create(not_finished_tasks)
                    print("Created {} task personals for {}".format(len(not_finished_tasks), komax_task_obj))
            else:
                if harnesses_number is None:
                    harnesses_numbers = dataframe['harness'].unique()
                    harnesses = dict()
                    for harness_number in harnesses_numbers:
                        harnesses[harness_number] = Harness.objects.filter(harness_number=harness_number)[0]
                else:
                    harnesses = dict()
                    for harness_number in harnesses_number:
                        harnesses[harness_number] = Harness.objects.filter(harness_number=harness_number)[0]

                # New type of loading
                task_pers_objs = list()
                for row in dataframe.iterrows():
                    row_dict = row[1]
                    task_pers_objs.append(
                        TaskPersonal(
                            komax_task=komax_task_obj,
                            # harness=get_object_or_404(Harness, harness_number=row_dict['harness']),
                            # komax=get_object_or_404(Komax, number=row_dict['komax']),
                            harness=harnesses[row_dict['harness']],
                            komax=None,
                            kappa=None,
                            amount=int(row_dict["amount"]),
                            notes=str(row_dict["notes"]),
                            marking=str(row_dict["marking"]),
                            wire_type=str(row_dict["wire_type"]),
                            wire_number=str(row_dict["wire_number"]),
                            wire_square=float(row_dict["wire_square"]),
                            wire_color=str(row_dict["wire_color"]),
                            wire_length=int(row_dict["wire_length"]),
                            tube_len_1=str(row_dict["tube_len_1"]),
                            wire_seal_1=str(row_dict["wire_seal_1"]),
                            wire_cut_length_1=float(row_dict["wire_cut_length_1"]),
                            wire_terminal_1=str(row_dict["wire_terminal_1"]),
                            aplicator_1=str(row_dict["aplicator_1"]),
                            tube_len_2=str(row_dict["tube_len_2"]),
                            wire_seal_2=str(row_dict["wire_seal_2"]),
                            wire_cut_length_2=float(row_dict["wire_cut_length_2"]),
                            wire_terminal_2=str(row_dict["wire_terminal_2"]),
                            aplicator_2=str(row_dict["aplicator_2"]),
                            # time=row_dict['time']
                        )
                    )
                TaskPersonal.objects.bulk_create(task_pers_objs)

    def __create_harness_amount_from_dataframe(self, komax_task, dataframe):
        komax_task_harnesses = komax_task.harnesses.all()
        harnesses_number_add = dataframe['harness'].unique()
        return

    def create_task_personal_from_dataframe_dict(self, dataframe_dict, worker=None, komax_number=None):
        if type(dataframe_dict) is dict and len(dataframe_dict):
            dataframe = pd.DataFrame.from_dict(dataframe_dict)
            dataframe.index = pd.Index(range(dataframe.shape[0]))
            komax_number = dataframe.loc[0, 'komax']
            harnesses_number = dataframe['harness'].unique()
            komax = Komax.objects.filter(number=komax_number)[0]
            komax_order = KomaxOrder.objects.filter(komax=komax)[0]
            komax_task_obj = komax_order.komax_task
            self.__create_task_personal_from_dataframe(dataframe, komax_task_obj, worker, komax_number, harnesses_number)


    # TODO: add comparison with base allocation
    def create_allocation(self, task_name):
        """
        allocate
        :param task_name:
        :return:
        """

        """
        task_query = get_komax_task(task_name=task_name)
        task_df = 0
        task_obj = 0
        if len(task_query):
            task_obj = task_query[0]
            task_df_query = get_task_personal(task_obj=task_query[0])
            if len(task_df_query):
                task_df = read_frame(task_df_query)
                
        

        if type(task_df) is int:
            return -1
        """
        task_obj = get_komax_task(task_name=task_name)[0]
        task_df = get_task_personal(task_obj, output='dataframe')
        """
        sorted_alloc = task_df['allocation'][0]
        alloc_base = alloc_chart_dict['allocation'][1]

        final_alloc = {komax: [1 - round(time/alloc_base[komax], 2)] for komax, time in sorted_alloc.items()}
        """

        amount_dict = self.__get_amount_dict(task_name)
        process = ProcessDataframe(task_df)
        harnesses, komax_dict, kappas, shift, type_of_allocation = self.get_params_from_komax_task(task_obj)
        time_dict = get_time_from(read_frame(get_laboriousness()))

        # amount_dict = get_amount_from(read_frame(task_obj.harnesses.all()))

        # alloc = process.task_allocation(komax_dict, quantity=None, time=time_dict, hours=shift)

        #TODO: increase efficiensy of func
        alloc = process.allocate(komax_dict, kappas, amount_dict, time_dict, shift, type_of_allocation)
        self.__update_task_personal_from_dataframe(process.chart, task_obj)

        if type(alloc) is int:
            task_obj.harnesses.all().delete()
            task_obj.komaxes.all().delete()
            task_obj.delete()
            TaskPersonal.objects.filter(komax_task=task_obj).delete()
            return alloc

        """
        komax_task_query = get_komax_task(task_name=task_name)
        komax_task = komax_task_query[0]
        komax_task_komaxes = get_komaxes(komax_task_obj=komax_task)

        for komax, time in alloc.items():
            alloc[komax] = list(alloc[komax])
            # alloc[komax].append((1 - round(sorted_alloc[komax]/alloc_base[komax])) * 100)
            for komax_time in komax_task_komaxes:
                komax_number = komax_time.komax.number
                if komax_number == komax:
                    komax_time.time = alloc[komax][0]
                    save_obj(komax_time)
                    break
        
        
            hours = round(alloc[komax][0] // 3600)
            # alloc[komax] = str(hours) + ':' + str(round((final_alloc[komax][0] / 3600 - hours) * 60))
            alloc[komax] = str(hours)

        return alloc
        
        """

        return alloc

    def delete_komax_order(self, komax_number):
        try:
            KomaxOrder.objects.filter(komax__number=komax_number).delete()
        except KomaxOrder.DoesNotExist:
            pass





