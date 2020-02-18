from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.views import generic
from django.urls import reverse_lazy
from .models import Harness, HarnessChart, Komax, Laboriousness, KomaxTask, HarnessAmount, TaskPersonal, \
    Tickets, KomaxTime, KomaxWork, Kappa, KomaxTerminal
from .forms import KomaxEditForm, KomaxCreateForm
from .modules.ioputter import FileReader
from django_pandas.io import read_frame
import pandas as pd
from .modules.HarnessChartProcessing import ProcessDataframe, get_komaxes_from, get_time_from, get_amount_from
import datetime
import openpyxl as xl
from openpyxl.utils.dataframe import dataframe_to_rows
from time import time
from django.db.models import Sum
from chartjs.views.lines import BaseLineChartView
from .modules.outer import OutProcess
from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt, requires_csrf_token
import time
from .task import get_wb_labels, save_tickets

from django.shortcuts import render, redirect, get_list_or_404, get_object_or_404, reverse
# from .models import Harness, HarnessChart, Komax, Laboriousness, KomaxTask
from django.views import View, generic
from .modules.HarnessChartProcessing import HarnessChartReader
# from .forms import KomaxTaskSetupForm, KomaxEditForm, KomaxCreateForm
from django.views import generic
from .task import create_allocation, sort_allocated_task
import time
from django.utils.timezone import now
from django.db import close_old_connections
from channels.db import database_sync_to_async

browser_useragents = ["ABrowse", "Acoo Browser", "America Online Browser", "AmigaVoyager", "AOL", "Arora",
                      "Avant Browser", "Beonex", "BonEcho", "Browzar", "Camino", "Charon", "Cheshire",
                      "Chimera", "Chrome", "ChromePlus", "Classilla", "CometBird", "Comodo_Dragon", "Conkeror",
                      "Crazy Browser", "Cyberdog", "Deepnet Explorer", "DeskBrowse", "Dillo", "Dooble", "Edge",
                      "Element Browser", "Elinks", "Enigma Browser", "EnigmaFox", "Epiphany", "Escape", "Firebird",
                      "Firefox", "Fireweb Navigator", "Flock", "Fluid", "Galaxy", "Galeon", "GranParadiso",
                      "GreenBrowser", "Hana", "HotJava", "IBM WebExplorer", "IBrowse", "iCab", "Iceape", "IceCat",
                      "Iceweasel", "iNet Browser", "Internet Explorer", "iRider", "Iron", "K-Meleon", "K-Ninja",
                      "Kapiko", "Kazehakase", "Kindle Browser", "KKman", "KMLite", "Konqueror", "LeechCraft", "Links",
                      "Lobo", "lolifox", "Lorentz", "Lunascape", "Lynx", "Madfox", "Maxthon", "Midori", "Minefield",
                      "Mozilla", "myibrow", "MyIE2", "Namoroka", "Navscape", "NCSA_Mosaic", "NetNewsWire",
                      "NetPositive", "Netscape", "NetSurf", "OmniWeb", "Opera", "Orca", "Oregano", "osb-browser",
                      "Palemoon", "Phoenix", "Pogo", "Prism", "QtWeb Internet Browser", "Rekonq", "retawq", "RockMelt",
                      "Safari", "SeaMonkey", "Shiira", "Shiretoko", "Sleipnir", "SlimBrowser", "Stainless", "Sundance",
                      "Sunrise", "surf", "Sylera", "Tencent Traveler", "TenFourFox", "theWorld Browser", "uzbl",
                      "Vimprobable", "Vonkeror", "w3m", "WeltweitimnetzBrowser", "WorldWideWeb", "Wyzo",
                      "Android Webkit Browser", "BlackBerry", "Blazer", "Bolt", "Browser for S60", "Doris", "Dorothy",
                      "Fennec", "Go Browser", "IE Mobile", "Iris", "Maemo Browser", "MIB", "Minimo", "NetFront",
                      "Opera Mini", "Opera Mobile", "SEMC-Browser", "Skyfire", "TeaShark", "Teleca-Obigo", "uZard Web",
                      "Thunderbird", "AbiLogicBot", "Link Valet", "Link Validity Check", "LinkExaminer",
                      "LinksManager.com_bot", "Mojoo Robot", "Notifixious", "online link validator", "Ploetz + Zeller",
                      "Reciprocal Link System PRO", "REL Link Checker Lite", "SiteBar", "Vivante Link Checker",
                      "W3C-checklink", "Xenu Link Sleuth", "EmailSiphon", "CSE HTML Validator", "CSSCheck", "Cynthia",
                      "HTMLParser", "P3P Validator", "W3C_CSS_Validator_JFouffa", "W3C_Validator", "WDG_Validator",
                      "Awasu", "Bloglines", "everyfeed-spider", "FeedFetcher-Google", "GreatNews", "Gregarius",
                      "MagpieRSS", "NFReader", "UniversalFeedParser", "!Susie", "Amaya", "Cocoal.icio.us",
                      "DomainsDB.net MetaCrawler", "gPodder", "GSiteCrawler", "iTunes", "lftp", "MetaURI",
                      "MT-NewsWatcher", "Nitro PDF", "Snoopy", "URD-MAGPIE", "WebCapture", "Windows-Media-Player"]

time_dict = {
        'learn': 150,
        'cut': 0.69,
        'aplicator': 190,
        'direction': 55,
        'contact': 95,
        'wire': 70,
        'compact': 360,
        'pack': 31,
        'ticket': 42,
        'task': 23,
    }


"""
def upload_harness_chart(request):
    if request.method == 'POST':
        form = Temp_chartForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('komax_app:harness')
    else:
        form = Temp_chartForm()
    return render(request, 'komax_app/upload_harness_chart.html', {
        'form': form
    })
"""

"""
def upload(request):
    context = {
        'form' : Temp_chartForm
    }
    if request.method == 'POST':
        uploaded_file = request.FILES['xlsx']
        fs = FileSystemStorage()
        name = fs.save(uploaded_file.name, uploaded_file)
        context['url'] = fs.url(name)
    return render(request, 'komax_app/upload_harness_chart.html', context)
"""

class KomaxTerminalsListView(View):
    template_name = 'komax_app/komax_terminals.html'

    def get(self, request, *args, **kwargs):
        komax_terminals = KomaxTerminal.objects.order_by('terminal_name')

        context = {
            'terminals': komax_terminals,
        }

        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        if 'terminal_name' in request.POST and 'availability' in request.POST:
            terminal_name = request.POST['terminal_name']
            availability = True if request.POST['availability'] == 'yes' else False

            KomaxTerminal(terminal_name=terminal_name, available=availability).save()

        elif 'Change' in request.POST:
            terminal_name = request.POST['terminal_name']
            komax_terminal_obj = KomaxTerminal.objects.filter(terminal_name=terminal_name)[0]
            komax_terminal_obj.available = not komax_terminal_obj.available
            komax_terminal_obj.save()

        elif 'Delete' in request.POST:
            terminal_name = request.POST['terminal_name']
            KomaxTerminal.objects.filter(terminal_name=terminal_name)[0].delete()

        return redirect('komax_app:komax_terminals_list')

class HarnessesListView(View):
    template_name = 'komax_app/harnesses.html'

    def get(self, request, *args, **kwargs):
        harnesses = Harness.objects.order_by('harness_number')

        context = {
            'harnesses': harnesses,
        }

        close_old_connections()

        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):

        reader = HarnessChartReader()
        reader.load_file(request.FILES['harness_chart'])
        reader.read_file_chart()

        harness_number = request.POST['harness_number']

        harness = Harness(harness_number=harness_number)
        harness.save()
        HarnessChart().save_from_dataframe(
            harness_dataframe=reader.get_dataframe(),
            harness_number=harness_number
        )
        close_old_connections()

        return redirect('komax_app:harnesses')

class EquipmentListView(View):
    template_name = 'komax_app/equipment.html'
    status = {
        1: 'Work',
        2: 'Repair',
        0: 'Not working'
    }
    marking = {
        1: 'Black',
        2: 'White',
        3: 'Both'
    }
    pairing = {
        0: 'No',
        1: 'Yes',
    }
    group_of_square = {
        1: '0.5 - 1.0',
        2: '1.5 - 2.5',
        3: '4.0 - 6.0'
    }

    def get(self, request, *args, **kwargs):
        komaxes = Komax.objects.order_by('number')

        komaxes_html = [
            (
                komax.number,
                self.status.get(komax.status),
                self.marking.get(komax.marking),
                self.pairing.get(komax.pairing),
                [self.group_of_square.get(group) for group in list(map(int, komax.group_of_square.split()))],
                komax.identifier
            )
            for komax in komaxes
        ]

        kappas = Kappa.objects.order_by('number')

        kappas_html = [
            (
                kappa.number,
                self.status.get(kappa.status)
            )
            for kappa in kappas
        ]

        context = {
            'komaxes': komaxes_html,
            'kappas': kappas_html,
            'komax_status': self.status.values(),
            'komax_marking': self.marking.values(),
            'komax_pairing': self.pairing.values(),
            'komax_group_of_square': self.group_of_square.values()
        }

        return render(request, self.template_name, context)

    #TODO: add reading feature of russian lang
    def post(self, request, *args, **kwargs):
        """
        correcting or adding komaxes
        :param request:
        :param args:
        :param kwargs:
        :return: None
        """

        number = request.POST['number']
        status = get_key(self.status, request.POST['status'])
        marking = get_key(self.marking, request.POST['marking'])
        pairing = get_key(self.pairing, request.POST['pairing'])
        identifier = request.POST['identifier']
        groups_of_square_text = request.POST.getlist('group_of_square')

        groups_of_square_int = list()
        for group_of_square_text in groups_of_square_text:
            group_of_square_int = get_key(self.group_of_square, group_of_square_text)
            groups_of_square_int.append(str(group_of_square_int))

        group_of_square = (' ').join(groups_of_square_int)

        if status is None or marking is None or pairing is None or identifier is None or group_of_square is None:
            return redirect('komax_app:komaxes')

        komax_query = Komax.objects.filter(number=number)

        if len(komax_query):
            komax = komax_query[0]
            komax.status = status
            komax.marking = marking
            komax.pairing = pairing
            komax.identifier = identifier
            komax.group_of_square = group_of_square
            komax.save()
        else:
            Komax(
                number=number,
                status=status,
                marking=marking,
                pairing=pairing,
                group_of_square=group_of_square,
                identifier=identifier
            ).save()

        return redirect('komax_app:komaxes')

class LaboriousnessListView(View):
    template_name = 'komax_app/laboriousness.html'

    def get(self, request, *args, **kwargs):
        laboriousness = Laboriousness.objects.all()

        if len(laboriousness) == 0:
            fulfill_time()

        close_old_connections()
        context = {
            'actions': laboriousness,
        }

        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        """
        add or change laboriousness

        :param request:
        :param args:
        :param kwargs:
        :return:
        """

class KomaxAppSetupView(View):
    template_name = 'komax_app/komax_app_setup.html'

    def get(self, request, *args, **kwargs):
        """
        show form
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        harnesses = Harness.objects.order_by('harness_number')
        komaxes = Komax.objects.order_by('number').filter(status=1)
        kappas = Kappa.objects.order_by('number').filter(status=1)

        context = {
            'harnesses': harnesses,
            'komaxes': komaxes,
            'kappas': kappas,
        }

        return render(request, self.template_name, context)


    def post(self, request, *args, **kwargs):
        """
        setup form with JQuery

        :param request:
        :param args:
        :param kwargs:
        :return:
        """

        print(request.POST)



        return redirect('komax_app:task_setup')

class TaskPersonalJsonView(View):

    def __error(self):
        return

    def get(self, request, identifier, *args, **kwargs):
        if not request_from_browser(request):
            if type(identifier) is not str:
                return self.__error()

            komax_query = Komax.objects.filter(identifier=identifier)
            if not len(komax_query):
                return self.__error()

            komax = komax_query[0]
            komax_work_query = KomaxWork.objects.filter(komax=komax)

            response_data = dict()

            if len(komax_work_query):
                komax_work = komax_work_query[0]
                komax_task = komax_work.komax_task
                task_personal_query = TaskPersonal.objects.filter(komax_task=komax_task, komax=komax)
                response_data = read_frame(task_personal_query).to_dict()

            return JsonResponse(response_data)
        else:
            return redirect('komax_app:task_setup')

    def post(self, *args, **kwargs):
        return

class KomaxTaskListView(View):
    template_name = 'komax_app/komax_tasks.html'

    def get(self, request):
        komax_tasks = KomaxTask.objects.order_by('-created')

        context = {
            'tasks': komax_tasks,
        }

        return render(request, self.template_name, context)

    def post(self, request):
        return redirect('komax_app:komax_task_list')

def get_key(dict, val, returns=None):
    for key, value in dict.items():
         if val == value:
             return key
    return returns

class KomaxEditView(generic.UpdateView):
    model = Komax
    form_class = KomaxEditForm
    context_object_name = 'komaxes'
    template_name = 'komax_app/komaxes_edit.html'
    # success_url = reverse_lazy('komax_app:komaxes')

def seconds_to_str_hours(seconds):
    """
    convert int seconds to str hours
    :param seconds: int
    :return: str of hours in format 16:54
    """
    hours = round(seconds // 3600)
    mins = round((seconds / 3600 - hours) * 60)

    if mins == 60:
        mins = 0
        hours += 1

    return str(hours) + ':' + str(mins)

class KomaxTaskView(View):
    model = KomaxTask

    def get(self, request, task_name, *args, **kwargs):
        task = get_object_or_404(self.model, task_name=task_name)
        harnesses = task.harnesses.all()
        status = 'success'
        komaxes_time = task.komaxes.all()
        final_alloc = {komax_time.komax.number: komax_time.time for komax_time in komaxes_time}
        kappas = [task.kappas, ]
        exceeds_shift = False


        for key, item in final_alloc.items():
            if final_alloc[key] / 3600 > task.shift:
                exceeds_shift = True
            final_alloc[key] = seconds_to_str_hours(final_alloc[key])


        context = {
            'task': task,
            'harnesses': harnesses,
            'alloc': final_alloc,
            'harness_amount': 12 // len(harnesses),
            'komaxes_amount': 12 // len(final_alloc),
            'exceeds_shift': exceeds_shift,
            'status': status,
            'kappas': kappas,
        }

        return render(request, 'komax_app/komax_app_task.html', context=context)

    def post(self, request, *args, **kwargs):
        close_old_connections()
        return redirect('komax_app:task_setup')

def get_harness_chart_view(request, harness_number):
    harness_obj = get_object_or_404(Harness, harness_number=harness_number)
    harness_chart_query = HarnessChart.objects.filter(harness=harness_obj)
    if len(harness_chart_query):
        harness_chart_df = read_frame(harness_chart_query)
    else:
        return redirect('komax_app:harnesses')

    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    )
    response['Content-Disposition'] = 'attachment; filename={}.xlsx'.format(harness_number)

    harness_chart_file = OutProcess(harness_chart_df)
    workbook = harness_chart_file.get_harness_chart_xl()
    workbook.save(response)

    return response

def get_personal_task_view_komax(request, task_name, komax):
    komax_obj = get_object_or_404(Komax, number=komax)
    tasks_obj = get_object_or_404(KomaxTask, task_name=task_name)
    task_pers_df = read_frame(TaskPersonal.objects.filter(komax_task=tasks_obj, komax=komax_obj))

    task_pers_df.sort_values(
        by=['id'],
        ascending=True,
        inplace=True,
    )

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

def get_general_task_view(request, task_name):
    task_pers_df = read_frame(TaskPersonal.objects.filter(komax_task=get_object_or_404(KomaxTask, task_name=task_name)))

    task_pers_df.sort_values(
        by=['id'],
        ascending=True,
        inplace=True,
    )

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
    workbook.save(response)

    return response

def get_personal_task_view_kappa(request, task_name, kappa):
    komax_task_obj = get_object_or_404(KomaxTask, task_name=task_name)

    kappa_task_pers_df = read_frame(TaskPersonal.objects.filter(komax_task=komax_task_obj, kappa=komax_task_obj.kappas))

    kappa_task_pers_df.sort_values(
        by=['id'],
        ascending=True,
        inplace=True,
    )

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
    workbook = out_file.get_task_xl()
    workbook.save(response)

    return response

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

def harness_delete(request, harness_number):
    harness_to_delete = Harness.objects.filter(harness_number=harness_number)
    if len(harness_to_delete) > 0:
        harness_to_delete.delete()
    close_old_connections()
    return redirect('komax_app:harnesses')

def fulfill_time():
    """
    Fulfills time to database

    :return: None
    """

    for key, item in time_dict.items():
        Laboriousness(action=key, time=item).save()

def request_from_browser(request):
    if any(browser_useragent in request.META['HTTP_USER_AGENT'] for browser_useragent in browser_useragents):
        return True
    else:
        return False

def handle_json_post(request):
    if not request_from_browser(request):
        pass
    else:
        return redirect('komax_app:task_setup')

@ensure_csrf_cookie
def handle_json_get(request, harness_number):
    if not request_from_browser(request):
        harness_obj = Harness.objects.filter(harness_number=harness_number)[0]
        data = read_frame(HarnessChart.objects.filter(harness=harness_obj)).to_dict()
        any(browser_useragent in request.META['HTTP_USER_AGENT'] for browser_useragent in browser_useragents)
        close_old_connections()
        return JsonResponse(data)
    else:
        close_old_connections()
        return redirect('komax_app:task_setup')

def handle_temp_chart(temp_chart):
    reader = FileReader(temp_chart)
    reader.read_file_chart()

    return reader.dataframe_file

def upload_temp_chart(request):
    context = {
        'form': HarnessChartUploadForm
    }
    if request.method == 'POST':
        form = HarnessChartUploadForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = request.FILES['xlsx']
            harness_number = request.POST['harness']
            chart_data = handle_temp_chart(uploaded_file)

            harness_obj = Harness(harness_number=harness_number)
            harness_obj.save()

            harness_chart_obj = 0
            error_ocured = False

            for row in chart_data.iterrows():
                row_dict = row[1]
                harness_chart_obj = HarnessChart(
                    harness=harness_obj,
                    notes=row_dict["Примечание"],
                    marking=row_dict["Маркировка"],
                    wire_type=row_dict["Вид провода"],
                    wire_number=row_dict["№ провода"],
                    wire_square=float(row_dict["Сечение"]),
                    wire_color=row_dict["Цвет"],
                    wire_length=int(row_dict["Длина, мм (± 3мм)"]),
                    wire_seal_1=row_dict["Уплотнитель 1"],
                    wire_cut_length_1=float(row_dict["Частичное снятие 1"]),
                    wire_terminal_1=row_dict["Наконечник 1"],
                    aplicator_1=row_dict["Аппликатор 1"],
                    tube_len_1=float(row_dict["Длина трубки, L (мм) 1"]),
                    armirovka_1=row_dict["Армировка 1 (Трубка ПВХ, Тр.Терм., изоляторы)"],
                    wire_seal_2=row_dict["Уплотнитель 2"],
                    wire_cut_length_2=float(row_dict["Частичное снятие 2"]),
                    wire_terminal_2=row_dict["Наконечник 2"],
                    aplicator_2=row_dict["Аппликатор 2"],
                    tube_len_2=float(row_dict["Длина трубки, L (мм) 2"]),
                    armirovka_2=row_dict["Армировка 2 (Трубка ПВХ, Тр.Терм., изоляторы)"]
                )

                if error_ocured:
                    harness_obj_to_delete = get_object_or_404(Harness, harness_number=harness_number)
                    harness_obj_to_delete.delete()
                    return HttpResponseRedirect('/komax_app/harnesses/')

                try:
                    harness_chart_obj.save()
                except ValueError:
                    error_ocured = True

                if error_ocured:
                    harness_obj_to_delete = get_object_or_404(Harness, harness_number=harness_number)
                    harness_obj_to_delete.delete()
                    try:
                        harness_chart_obj.delete()
                    except:
                        pass

                    return HttpResponseRedirect('/komax_app/harnesses/')


            return HttpResponseRedirect('/komax_app/harnesses/')
    else:
        form = HarnessChartUploadForm
    return render(request, 'komax_app/upload_harness_chart.html', context)

def harness_chart_view(request, pk):
    try:
        obj = get_list_or_404(HarnessChart, harness_id=get_object_or_404(Harness, harness_number=pk))
    except:
        raise Http404('Not found Harness of Harness charts or returned list of Harnesses by this id')
    context = {
        'harness_number': pk,
        'positions': obj
    }
    close_old_connections()
    return render(request, 'komax_app/chart_view.html', context)

def set_amount_task_view(request, pk):
    tasks_objs = KomaxTask.objects.filter(task_name=pk)
    harnesses = 0

    if len(tasks_objs) > 0:
        harnesses = tasks_objs[0].harnesses.all()
    else:
        return redirect('komax_app:task_setup')

    harness_numbers = list()
    for harness in harnesses:
        harness_numbers.append(harness.harness)

    if request.method == 'POST':
        for harness_number in harness_numbers:
            amount = request.POST['amount-' + harness_number.harness_number]
            harness = request.POST['' + harness_number.harness_number]

            obj = get_object_or_404(KomaxTask, task_name=pk)
            obj.save()
            harnesses_tasks_obj = obj.harnesses.filter(harness=harness)[0]
            harnesses_tasks_obj.amount = amount
            harnesses_tasks_obj.save()


        return redirect('komax_app:task_view', pk=pk)

    elif request.method == 'GET' and harness_numbers:

        context = {
            'harnesses': harness_numbers,
        }
        return render(request, 'komax_app/komax_app_amount.html', context)
    else:
        return redirect('komax_app:task_setup')

class KomaxTaskProcessing():

    def __init__(self):
        return

    def save_obj(self, obj):
        obj.save()

    def get_komax_task(self, task_name):
        return KomaxTask.objects.filter(task_name=task_name)

    def get_harnesses(self, komax_task_obj=None, harness=None):
        if komax_task_obj is None:
            if harness is None:
                return Harness.objects.all()
            else:
                return Harness.objects.filter(harness_number=harness)
        else:
            return komax_task_obj.harnesses.all()

    def get_komaxes(self, komax_task_obj=None, komax=None):
        if komax_task_obj is None:
            if komax is None:
                return Komax.objects.all()
            else:
                return Komax.objects.filter(number=komax)
        else:
            return komax_task_obj.komaxes.all()

    def get_shift(self, komax_task_obj):
        return komax_task_obj.shift

    def get_harness_chart(self, harness_obj=None):
        if harness_obj is not None:
            return HarnessChart.objects.filter(harness=harness_obj)
        else:
            return HarnessChart.objects.all()

    def get_task_personal(self, task_obj=None):
        if task_obj is None:
            return TaskPersonal.objects.all()
        else:
            return TaskPersonal.objects.filter(komax_task=task_obj)

    def get_laboriousness(self):
        return Laboriousness.objects.all()

    def get_kappas(self, kappa_number=1):
        if kappa_number is None:
            return [None, ]
        else:
            return Kappa.objects.filter(number=kappa_number)

    def get_komax_terminls(self):
        return KomaxTerminal.objects.all()

    def create_harness_amount(self, harnesses, amount=-1):
        harness_amount_objs = list()
        for harness in harnesses:
            harness_amount_obj = HarnessAmount(harness=Harness.objects.filter(harness_number=harness)[0], amount=amount)
            harness_amount_objs.append(harness_amount_obj)
            self.save_obj(harness_amount_obj)

        return harness_amount_objs

    def create_komax_time(self, komaxes, time=0):
        komax_time_objs = list()
        for komax in komaxes:
            komax_time_obj = KomaxTime(komax=Komax.objects.filter(number=komax)[0], time=time)
            komax_time_objs.append(komax_time_obj)
            self.save_obj(komax_time_obj)

        return komax_time_objs

    def create_task(self, task_name, harnesses, komaxes, kappas, shift, type_of_allocation):
        harness_amount_objs = self.create_harness_amount(harnesses)
        komax_time_objs = self.create_komax_time(komaxes)
        komax_task_obj = KomaxTask(
            task_name=task_name,
            kappas=self.get_kappas(kappas[0])[0],
            shift=shift,
            type_of_allocation=type_of_allocation
        )
        self.save_obj(komax_task_obj)
        komax_task_obj.harnesses.add(*harness_amount_objs)
        komax_task_obj.komaxes.add(*komax_time_objs)
        self.save_obj(komax_task_obj)

    def update_harness_amount(self, task_name, harness_amount_dict):
        task_query = self.get_komax_task(task_name)
        task = task_query[0]
        harnesses = self.get_harnesses(task)
        for harness in harnesses:
            harness.amount = harness_amount_dict[str(harness)]
            self.save_obj(harness)

        tasks_pers = self.get_task_personal(task)

        for task_pers in tasks_pers:
            task_pers.amount = harness_amount_dict[str(task_pers.harness.harness_number)]
            self.save_obj(task_pers)

    def update_komax_time(self, task_name, komax_time_dict):
        task_query = self.get_komax_task(task_name=task_name)
        task = task_query[0]
        komaxes = self.get_komaxes(komax_task_obj=task)
        for komax in komaxes:
            komax.amount = komax_time_dict[str(komax)]
            self.save_obj(komax)

    def __get_komaxes_from(self, komax_df):
        temp_dict = komax_df.to_dict()
        output_dict = {}
        for idx, komax_num in temp_dict['komax'].items():
            komax = self.get_komaxes(komax=komax_num)[0]
            status = komax.status
            marking = komax.marking
            pairing = komax.pairing
            groups_of_square = tuple(map(int, komax.group_of_square.split()))

            output_dict[int(komax_num)] = (status, marking, pairing, groups_of_square)

        return output_dict

    def sort_komax_task(self, task_name):
        """
        sort komax task
        :param task_name:
        :param type_of_allocation: str, parallel or consistently
        :return:
        """
        task_query = self.get_komax_task(task_name)
        task_obj = task_query[0]
        harnesses_query = self.get_harnesses(komax_task_obj=task_obj)
        komaxes_query = self.get_komaxes(komax_task_obj=task_obj)
        kappas = [task_obj.kappas]

        shift = self.get_shift(task_obj)
        harnesses = harnesses_query

        harness_charts = list()
        for harness in harnesses:
            harness_chart = self.get_harness_chart(harness_obj=harness.harness)
            harness_charts.append(harness_chart)

        df = pd.concat(
            [read_frame(harness_chart) for harness_chart in harness_charts],
            ignore_index=True
        )

        laboriousness = self.get_laboriousness()
        komax_dict = self.__get_komaxes_from(read_frame(komaxes_query))
        time_dict = get_time_from(read_frame(laboriousness))
        type_of_allocation = task_obj.type_of_allocation
        terminals_df = read_frame(self.get_komax_terminls())

        # amount_dict = get_amount_from(read_frame(task_obj.harnesses.all()))

        # print(df, komax_dict, harnesses, time_dict, shift)
        final_data = self.__sort_allocated_task(
            df,
            terminals_df,
            komax_dict,
            kappas,
            harnesses,
            time_dict,
            shift,
            type_of_allocation
        )

        self.sort_alloc_data = final_data

        if final_data['allocation'][0] == -1:
            task_obj.harnesses.all().delete()
            task_obj.komaxes.all().delete()
            task_obj.delete()
            return final_data

        """
        final_data['chart'].drop(
            columns=['tube_len_2', 'tube_len_1', 'armirovka_2', 'armirovka_1', 'id'],
            inplace=True
        )
        """

        for row in final_data['chart'].iterrows():
            row_dict = row[1]
            harness_obj = self.get_harnesses(harness=row_dict['harness'])[0]
            if row_dict['komax'] is None:
                komax_obj = None
            else:
                komax_obj = self.get_komaxes(komax=row_dict['komax'])[0]
            kappa_obj = self.get_kappas(kappa_number=row_dict['kappa'])[0]
            self.save_task_personal(row_dict, task_obj, kappa_obj, harness_obj, komax_obj)

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
        return final_data

    def save_task_personal(self, row_dict, task_obj, kappa_obj, harness_obj, komax_obj):
        task_pers_obj = TaskPersonal(
            komax_task=task_obj,
            # harness=get_object_or_404(Harness, harness_number=row_dict['harness']),
            # komax=get_object_or_404(Komax, number=row_dict['komax']),
            harness=harness_obj,
            komax=komax_obj,
            kappa=kappa_obj,
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

    def __sort_allocated_task(self, df, terminals_df, komax_dict, kappas, harnesses, time_dict, shift,
                              type_of_allocaton='parallel'):

        process = ProcessDataframe(df)
        process.filter_availability_komax_terminal(terminals_df)

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

    def __get_amount_dict(self, task_name):
        komax_task_query = self.get_komax_task(task_name)
        komax_task = komax_task_query[0]
        komax_task_harnesses = self.get_harnesses(komax_task_obj=komax_task)
        return {harness.harness.harness_number: harness.amount for harness in komax_task_harnesses}

    # TODO: add comparison with base allocation
    def create_allocation(self, task_name):
        """
        allocate
        :param task_name:
        :param type_of_allocation: str, parallel or consistently
        :return:
        """

        task_query = self.get_komax_task(task_name=task_name)
        task_df = 0
        task_obj = 0
        if len(task_query):
            task_obj = task_query[0]
            task_df_query = self.get_task_personal(task_obj=task_query[0])
            if len(task_df_query):
                task_df = read_frame(task_df_query)

        if type(task_df) is int:
            return -1

        task_df.sort_values(
            by=['id'],
            ascending=True,
            inplace=True,
        )

        task_df.index = pd.Index(range(task_df.shape[0]))

        amount_dict = self.__get_amount_dict(task_name)
        """
        sorted_alloc = task_df['allocation'][0]
        alloc_base = alloc_chart_dict['allocation'][1]
        
        final_alloc = {komax: [1 - round(time/alloc_base[komax], 2)] for komax, time in sorted_alloc.items()}
        """
        final_chart = task_df
        process = ProcessDataframe(final_chart)

        shift = self.get_shift(komax_task_obj=task_obj)
        komaxes_query = self.get_komaxes(komax_task_obj=task_obj)
        komaxes = komaxes_query
        laboriousness_query = self.get_laboriousness()
        laboriousness = laboriousness_query
        komax_dict = self.__get_komaxes_from(read_frame(komaxes))
        time_dict = get_time_from(read_frame(laboriousness))
        kappas = [task_obj.kappas, ]
        type_of_allocation = task_obj.type_of_allocation

        # amount_dict = get_amount_from(read_frame(task_obj.harnesses.all()))

        # alloc = process.task_allocation(komax_dict, quantity=None, time=time_dict, hours=shift)


        alloc = process.allocate(komax_dict, kappas, amount_dict, time_dict, shift, type_of_allocation)

        if type(alloc) is int:
            task_obj.harnesses.all().delete()
            task_obj.komaxes.all().delete()
            task_obj.delete()
            TaskPersonal.objects.filter(komax_task=task_obj).delete()
            return alloc

        komax_task_query = self.get_komax_task(task_name=task_name)
        komax_task = komax_task_query[0]
        komax_task_komaxes = self.get_komaxes(komax_task_obj=komax_task)

        for komax, time in alloc.items():
            alloc[komax] = list(alloc[komax])
            # alloc[komax].append((1 - round(sorted_alloc[komax]/alloc_base[komax])) * 100)
            for komax_time in komax_task_komaxes:
                komax_number = komax_time.komax.number
                if komax_number == komax:
                    komax_time.time = alloc[komax][0]
                    self.save_obj(komax_time)
                    break

            hours = round(alloc[komax][0] // 3600)
            # alloc[komax] = str(hours) + ':' + str(round((final_alloc[komax][0] / 3600 - hours) * 60))
            alloc[komax] = str(hours)

        return alloc

def create_task_view(request):
    context = {
        'form' : KomaxTaskSetupForm
    }
    if request.method == 'POST':
        form = KomaxTaskSetupForm(request.POST)
        if form.is_valid():
            # delete empty tasks
            HarnessAmount.objects.filter(amount=-1).delete()
            name = request.POST['task_name']
            harnesses = request.POST.getlist('harnesses')
            komaxes = request.POST.getlist('komaxes')
            shift = int(request.POST['shift'])

            # create task
            task_obj = KomaxTask(shift=0)
            task_obj.save()
            harnesses_task_objs = []

            for harness in harnesses:
                obj = HarnessAmount(harness=Harness.objects.get(id=harness), amount=-1)
                obj.save()
                harnesses_task_objs.append(obj)

            task_obj.harnesses.add(*harnesses_task_objs)
            task_obj.komaxes.add(*komaxes)
            task_obj.task_name = name
            task_obj.shift = shift
            task_obj.save()

            return HttpResponseRedirect('/komax_app/' + name + '/amount')

    return render(request, 'komax_app/komax_app_setup.html', context)

def get_task_view(request, pk):
    task_pers_df = read_frame(TaskPersonal.objects.filter(komax_task=get_object_or_404(KomaxTask, task_name=pk)))

    task_pers_df['done'] = ''
    alloc_df = read_frame(KomaxTaskAllocation.objects.filter(task=get_object_or_404(KomaxTask, task_name=pk)))
    alloc_df.drop(
        columns=['id'],
        inplace=True
    )

    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    )
    response['Content-Disposition'] = 'attachment; filename={task_name}.xlsx'.format(
        task_name=pk,
    )

    out_file = OutProcess(task_pers_df)
    workbook = out_file.get_task_xl()
    workbook.save(response)

    return response

def get_spec_task_view(request, pk, komax):
    komax_obj = get_object_or_404(Komax, number=komax)
    tasks_obj = get_object_or_404(KomaxTask, task_name=pk)
    task_pers_df = read_frame(TaskPersonal.objects.filter(komax_task=tasks_obj, komax=komax_obj))
    task_pers_df['done'] = ''

    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    )
    response['Content-Disposition'] = 'attachment; filename={task_name}-{komax_number}.xlsx'.format(
        task_name=pk,
        komax_number=komax,
    )
    out_file = OutProcess(task_pers_df)
    workbook = out_file.get_task_xl()
    workbook.save(response)
    close_old_connections()
    return response

def fulfill_time():
    """
    Fulfills time to database

    :return: None
    """

    for key, item in time_dict.items():
        Laboriousness(action=key, time=item).save()

def task_view(request, pk):

    if len(Laboriousness.objects.all()) == 0:
        fulfill_time()

    task_obj_query = KomaxTask.objects.filter(task_name=pk)

    if len(task_obj_query) > 0:
        task_obj = task_obj_query[0]

        amount_less_zero = True
        for harness in task_obj.harnesses.all():

            if harness.amount <= 0:
                amount_less_zero = True
                break
            else:
                amount_less_zero = False
                break



        status = 'success'
        if amount_less_zero:
            return redirect('komax_app:task_amount', pk=pk)
        else:
            task_pers_query = TaskPersonal.objects.filter(komax_task=task_obj_query[0])
            if len(task_pers_query) > 0:
                task_pers_obj = task_pers_query[0]
                harnesses = task_obj.harnesses.all()
                final_alloc = {}
                alloc_objs = get_list_or_404(KomaxTaskAllocation, task=task_obj)
                for alloc_obj in alloc_objs:
                    final_alloc[alloc_obj.komax.number] = [alloc_obj.time]
                alloc_base = {komax_number: [0] for komax_number in final_alloc}
                status = 'success'
            else:

                shift = task_obj.shift
                komaxes = task_obj.komaxes.all()
                harnesses = task_obj.harnesses.all()

                charts_df = []
                for harness in harnesses:
                    temp_df = read_frame(HarnessChart.objects.filter(harness=harness.harness))
                    charts_df.append(temp_df)

                df = pd.concat(charts_df, ignore_index=True)
                komax_df = read_frame(komaxes)
                time_df = read_frame(Laboriousness.objects.all())
                amount_df = read_frame(task_obj.harnesses.all())

                komax_dict = get_komaxes_from(komax_df)
                time_dict = get_time_from(time_df)
                amount_dict = get_amount_from(amount_df)

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
                        komax_task=task_obj,
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

            context = {
                'name': str(pk),
                'harnesses': harnesses,
                'alloc': final_alloc,
                'harness_amount': 12 // len(harnesses),
                'komaxes_amount': 12 // len(final_alloc),
                'status': status
            }

            return render(request, 'komax_app/komax_app_task.html', context=context)
    else:
        return redirect('komax_app:task_setup')

def komax_app_view(request):
    tasks = KomaxTask.objects.count()
    harnesses = Harness.objects.count()
    tasks_time = KomaxTime.objects.aggregate(Sum('time'))
    sum_time_task = 0
    if tasks_time['time__sum'] is not None:
        sum_time_task = tasks_time['time__sum'] // 3600
    context = {
        'tasks': tasks,
        'harnesses': harnesses,
        'tasks_time': round(sum_time_task)
    }
    return render(request, 'komax_app/komax_app_view.html', context=context)

def delete_harness_view(request, harness_number):
    harness_obj = Harness.objects.filter(harness_number=harness_number)
    if len(harness_obj) > 0:
        harnesses_tasks_obj = HarnessAmount.objects.filter(harness=harness_obj[0])
        if len(harnesses_tasks_obj) > 0:
            tasks_obj = KomaxTask.objects.filter(harnesses=harnesses_tasks_obj[0])
            tasks_obj.delete()
        harnesses_tasks_obj.delete()
        harness_obj.delete()

    return redirect('komax_app:harness')

def get_ticket_view(request, pk, komax):
    komax_obj = get_object_or_404(Komax, number=komax)
    tasks_obj = get_object_or_404(KomaxTask, task_name=pk)
    task_pers_df = read_frame(TaskPersonal.objects.filter(komax_task=tasks_obj, komax=komax_obj))

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
"""
def list_harness_view(request):
    if request.method == 'POST':
        form = HarnessChartUploadForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = request.FILES['xlsx']
            harness_number = request.POST['harness']
            chart_data = handle_temp_chart(uploaded_file)

            harness_obj = Harness(harness_number=harness_number)
            harness_obj.save()

            error_ocured = False

            for row in chart_data.iterrows():
                row_dict = row[1]
                harness_chart_obj = HarnessChart(
                    harness=harness_obj,
                    notes=row_dict["Примечание"],
                    marking=row_dict["Маркировка"],
                    wire_type=row_dict["Вид провода"],
                    wire_number=row_dict["№ провода"],
                    wire_square=float(row_dict["Сечение"]),
                    wire_color=row_dict["Цвет"],
                    wire_length=int(row_dict["Длина, мм (± 3мм)"]),
                    wire_seal_1=row_dict["Уплотнитель 1"],
                    wire_cut_length_1=float(row_dict["Частичное снятие 1"]),
                    wire_terminal_1=row_dict["Наконечник 1"],
                    aplicator_1=row_dict["Аппликатор 1"],
                    tube_len_1=float(row_dict["Длина трубки, L (мм) 1"]),
                    armirovka_1=row_dict["Армировка 1 (Трубка ПВХ, Тр.Терм., изоляторы)"],
                    wire_seal_2=row_dict["Уплотнитель 2"],
                    wire_cut_length_2=float(row_dict["Частичное снятие 2"]),
                    wire_terminal_2=row_dict["Наконечник 2"],
                    aplicator_2=row_dict["Аппликатор 2"],
                    tube_len_2=float(row_dict["Длина трубки, L (мм) 2"]),
                    armirovka_2=row_dict["Армировка 2 (Трубка ПВХ, Тр.Терм., изоляторы)"]
                )

                if error_ocured:
                    harness_obj_to_delete = get_object_or_404(Harness, harness_number=harness_number)
                    harness_obj_to_delete.delete()
                    return HttpResponseRedirect('/komax_app/harnesses/')

                try:
                    harness_chart_obj.save()
                except ValueError:
                    error_ocured = True

                if error_ocured:
                    harness_obj_to_delete = get_object_or_404(Harness, harness_number=harness_number)
                    harness_obj_to_delete.delete()
                    try:
                        harness_chart_obj.delete()
                    except:
                        pass

    harnesses = get_list_or_404(Harness)
    print(harnesses)
    context = {
        'harnesses': harnesses,
        'form': HarnessChartUploadForm,
    }

    return render(request, 'komax_app/harnesses.html', context)
"""
"""
class CreateTaskView(generic.CreateView):
    model = KomaxTask
    form_class = KomaxTaskSetupForm
    template_name = 'komax_app/komax_app_setup.html'
    success_url = reverse_lazy('komax_app:task_setup')

class KomaxesUpdateView(generic.UpdateView):
    model = Komax
    form_class = Komaxes_edit_form
    context_object_name = 'komaxes'
    template_name = 'komax_app/komaxes_edit.html'
    success_url = reverse_lazy('komax_app:komaxes')

class KomaxesView(generic.ListView):
    template_name = 'komax_app/equipment.html'
    model = Komax
    context_object_name = 'komaxes'

class HarnessView(generic.ListView):
    template_name = 'komax_app/harnesses.html'
    model = Harness
    context_object_name = 'harness'

class UploadHarnessChartView(generic.CreateView):
    template_name = 'komax_app/upload_harness_chart.html'
    model = Temp_chart
    form_class = HarnessChartUploadForm
    success_url = reverse_lazy('komax_app:harness')

class LabourisnessView(generic.ListView):
    model = Laboriousness
    template_name = 'komax_app/laboriousness.html'
    context_object_name = 'actions'
"""