from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect
from django_pandas.io import read_frame
from .modules.outer import OutProcess
from .celery import app
from .models import Tickets, Komax, KomaxTask, TaskPersonal
from django.core.files import File
from django.core.files.storage import FileSystemStorage
from openpyxl import load_workbook
import pandas as pd
from .modules.HarnessChartProcessing import ProcessDataframe
from .modules.process import ProcessDataframe, get_komaxes_from, get_time_from, get_amount_from


def get_wb_labels(task_pers_df):
    out_file = OutProcess(task_pers_df)
    wb = out_file.get_labels()

    return wb

@app.task
def sort_allocated_task(df, komax_dict, harnesses, time_dict, shift):
    process = ProcessDataframe(df)

    amount_dict = {harness: 1 for harness in harnesses}
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

def create_allocation(task_name, alloc_chart_dict):
    if alloc_chart_dict['allocation'][0] == -1:
        return -1

    final_alloc = alloc_chart_dict['allocation'][0]
    alloc_base = alloc_chart_dict['allocation'][1]

    final_chart = alloc_chart_dict['chart']
    final_chart.drop(
        columns=['tube_len_2', 'tube_len_1', 'armirovka_2', 'armirovka_1', 'id'],
        inplace=True
    )

    komax_task = KomaxTask.objects.filter(task_name=task_name)[0]

    TaskPersonal().save_from_df(
        dataframe=final_chart,
        komax_task=komax_task
    )

    for komax, time in final_alloc.items():
        KomaxTaskAllocation(task=komax_task, komax=get_object_or_404(Komax, number=komax), time=time[0]).save()


    for key, item in final_alloc.items():
        hours = round(final_alloc[key][0] // 3600)
        final_alloc[key] = str(hours) + ':' + str(round((final_alloc[key][0] / 3600 - hours) * 60))

    for key, item in alloc_base.items():
        hours = round(alloc_base[key][0] // 3600)
        alloc_base[key] = str(hours) + ':' + str(round((alloc_base[key][0] / 3600 - hours) * 60))

    for key, item in final_alloc.items():
        final_alloc[key] = [final_alloc[key], alloc_base[key]]

    return final_alloc

@app.task
def create_task_allocation_full(df, komax_dict, amount_dict, time_dict, shift, task_name):
    alloc_chart_dict = sort_allocate_task(df, komax_dict, amount_dict, time_dict, shift)
    allocation = create_allocation(task_name, alloc_chart_dict)

@app.task
def save_tickets(pk, komax_numbers):
    for komax in komax_numbers:
        komax_obj = get_object_or_404(Komax, number=komax)
        tasks_obj = get_object_or_404(KomaxTask, task_name=pk)
        task_pers_df = read_frame(TaskPersonal.objects.filter(task=tasks_obj, komax=komax_obj))
        wb = get_wb_labels(task_pers_df)
        filename = '{}-{}.xlsx'.format(pk, komax)
        tickets_obj = Tickets()
        tickets_obj.name = filename
        tickets_obj.labels = pd.ExcelWriter(wb)
        tickets_obj.save()
        """
        # wb.save(file)
        tickets_obj = Tickets(labels=name)
        tickets_obj.save()
        tickets_obj = Tickets.objects.filter(labels=wb)
        tickets_obj.name = '{}-{}'.format(pk, komax)"""


