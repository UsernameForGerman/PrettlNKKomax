# django libs
from django.http import Http404, HttpResponse
from django_pandas.io import read_frame
from django.views.generic import CreateView, UpdateView, DeleteView
from django.db.models import Sum
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_list_or_404, get_object_or_404
from django.views import View
from .modules.HarnessChartProcessing import HarnessChartReader
from django.views import generic
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.utils import translation
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt

# project libs
from .models import Harness, HarnessChart, Komax, Laboriousness, KomaxTask, HarnessAmount, TaskPersonal, \
    Tickets, KomaxTime, KomaxWork, Kappa, KomaxTerminal, OrderedKomaxTask, Worker, KomaxOrder, KomaxSeal
from .forms import KomaxEditForm
from .modules.KomaxTaskProcessing import get_task_personal, get_komax_task, KomaxTaskProcessing, get_task_to_load, \
    delete_komax_order, stop_komax_task_on_komax, update_komax_task_status, get_komax_task_status_on_komax
from .modules.outer import OutProcess
from .modules.KomaxCore import create_update_komax_status, get_komax_order, save_komax_task_personal, \
    delete_komax_status

# others
import pandas as pd
import json

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

def must_be_operator(user):
    return user.groups.filter(name='Operator').count()

def must_be_master(user):
    return user.groups.filter(name='Master').count()

@login_required
@permission_required('komax_app.add_orderedkomaxtask', raise_exception=True)
def send_task_to_worker(request, task_name, *args, **kwargs):
    task_obj = get_object_or_404(KomaxTask, task_name=task_name)
    task_obj.status = 2
    task_obj.save(update_fields=['status'])

    return redirect('komax_app:tasks_view')

@login_required
@permission_required('komax_app.delete_komaxtask')
def delete_task(request, task_name, *args, **kwargs):
    task_obj = get_object_or_404(KomaxTask, task_name=task_name)
    task_obj.delete()

    return redirect('komax_app:tasks_view')

def stop_komax_task(request, task_name, *args, **kwargs):
    task_obj = get_object_or_404(KomaxTask, task_name=task_name)
    for komax in task_obj.komaxes.all():
        stop_komax_task_on_komax(komax.komax, task_obj)
        if TaskPersonal.objects.filter(komax=komax.komax, loaded=True, komax_task=task_obj).exists():
            KomaxOrder.objects.create(komax_task=task_obj, komax=komax.komax, status="Requested")
        else:
            pass

    return redirect('komax_app:tasks_view')

@login_required
@permission_required('komax_app.change_taskpersonal')
def load_task_to_komax(request, task_name, *args, **kwargs):
    komax_num = request.session.get('komax', None)
    komax = get_object_or_404(Komax, number=komax_num)
    komax_task = get_object_or_404(KomaxTask, task_name=task_name)
    old_komax_tasks_id = TaskPersonal.objects.filter(
        loaded=True,
        komax=komax
    ).exclude(
        komax_task=komax_task
    ).values_list(
        'komax_task',
        flat=True
    ).distinct()

    old_komax_tasks = KomaxTask.objects.filter(id__in=old_komax_tasks_id)
    if len(old_komax_tasks):
        return Http404()
    processor = KomaxTaskProcessing()
    processor.load_task_personal(task_name, komax_num)
    KomaxOrder.objects.create(komax_task=komax_task, komax=komax, status='Received')

    update_komax_task_status(komax_task)


    return redirect('komax_app:user_account')

class WorkerAccountView(LoginRequiredMixin, View):
    template_name = 'komax_app/user_account.html'

    def get(self, request, *args, **kwargs):
        available_komaxes = Komax.objects.filter(status=1)
        worker = get_object_or_404(Worker, user=request.user)
        if worker.user.groups.filter(name='Operator').exists():
            komax_num = request.session.get('komax', None)
            if komax_num is None:
                context = {
                    'worker': worker,
                    'request_komax_num': True,
                    'available_komaxes': available_komaxes,
                }

                return render(request, self.template_name, context=context)
            else:
                worker.current_komax = get_object_or_404(Komax, number=komax_num)
                worker.save()
                ordered_komax_tasks = KomaxTask.objects.filter(komaxes__komax__number__exact=komax_num)\
                    .exclude(status=1).order_by('-created')

                komax_tasks_dict = dict()
                #TODO оптимизировать запросы
                for komax_task in ordered_komax_tasks:
                    komax_tasks_dict[komax_task] = [
                        komax_task.komaxes.filter(komax__number__exact=komax_num).first(),
                        get_komax_task_status_on_komax(komax_task, komax_num)
                    ]
                    komax_tasks_dict[komax_task][0].time = seconds_to_str_hours(komax_tasks_dict[komax_task][0].time)

                context = {
                    'worker': worker,
                    'komax_tasks': komax_tasks_dict,
                    'komax_num': komax_num,
                }
                return render(request, self.template_name, context=context)

        elif worker.user.groups.filter(name='Master').exists():
            komax_task_obj = KomaxTask.objects.filter(status=3).first()
            context = {
                'komax_task': komax_task_obj,
                'worker': worker,
            }

            return render(request, self.template_name, context=context)

    def post(self, request, *args, **kwargs):
        worker = get_object_or_404(Worker, user=request.user)
        if 'komax' in request.POST:
            request.session['komax'] = request.POST['komax']

        if 'language' in request.POST:
            request.session[translation.LANGUAGE_SESSION_KEY] = request.POST['language']

        if 'image' in request.FILES:
            worker.image = request.FILES['image']
            worker.save(update_fields=['image'])

        # redirect to GET user private acc
        return redirect('komax_app:user_account')

@method_decorator(user_passes_test(must_be_master), name='dispatch')
class TasksView(LoginRequiredMixin, View):
    template_name = 'komax_app/tasks.html'

    def get(self, request, *args, **kwargs):
        worker = get_object_or_404(Worker, user=request.user)

        komax_tasks = KomaxTask.objects.all().order_by('-created')

        context = {
            'komax_tasks': komax_tasks,
        }
        return render(request, self.template_name, context=context)

    def post(self, request, *args, **kwargs):

        # redirect to GET user private acc
        return redirect('komax_app:user_account')

class KomaxTerminalsListView(LoginRequiredMixin, View):
    template_name = 'komax_app/komax_terminals.html'

    @method_decorator(permission_required('komax_app.view_komaxterminal'))
    def get(self, request, *args, **kwargs):
        komax_terminals = KomaxTerminal.objects.order_by('terminal_name')

        context = {
            'terminals': komax_terminals,
        }

        return render(request, self.template_name, context)

    @method_decorator(user_passes_test(must_be_master))
    def post(self, request, *args, **kwargs):
        if 'Delete' in request.POST:
            terminal_name = request.POST['terminal-name']

            KomaxTerminal.objects.filter(terminal_name=terminal_name)[0].delete()

        else:
            terminal_name = request.POST['terminal-name']
            terminal = True if request.POST['terminal'] == '+' else False
            seal = True if request.POST['seal'] == '+' else False


            komax_query = KomaxTerminal.objects.filter(terminal_name=terminal_name)

            if len(komax_query):
                komax_obj = komax_query[0]
                komax_obj.terminal_available = terminal
                komax_obj.seal_installed = seal
                komax_obj.save()
            else:
                KomaxTerminal(terminal_name=terminal_name, terminal_available=terminal, seal_installed=seal).save()


        """
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
        """

        return redirect('komax_app:komax_terminals_list')

class KomaxSealsListView(LoginRequiredMixin, View):
    template_name = 'komax_app/komax_seals.html'

    @method_decorator(permission_required('komax_app.view_komaxseal'))
    def get(self, request, *args, **kwargs):
        komax_seals = KomaxSeal.objects.order_by('seal_name')

        context = {
            'seals': komax_seals,
        }

        return render(request, self.template_name, context)

    @method_decorator(user_passes_test(must_be_master))
    def post(self, request, *args, **kwargs):
        if 'Delete' in request.POST:
            seal_name = request.POST['seal-name']

            KomaxSeal.objects.filter(seal_name=seal_name)[0].delete()

        else:
            seal_name = request.POST['seal-name']
            seal = True if request.POST['seal'] == '+' else False


            komax_query = KomaxSeal.objects.filter(seal_name=seal_name)

            if len(komax_query):
                komax_obj = komax_query[0]
                komax_obj.seal_available = seal
                komax_obj.save()
            else:
                KomaxSeal(seal_name=seal_name, seal_available=seal).save()


        """
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
        """

        return redirect('komax_app:komax_seals_list')


class HarnessesListView(LoginRequiredMixin, View):
    template_name = 'komax_app/harnesses.html'

    @method_decorator(permission_required('komax_app.view_harness'))
    def get(self, request, *args, **kwargs):
        harnesses = Harness.objects.order_by('harness_number')

        context = {
            'harnesses': harnesses,
        }

        return render(request, self.template_name, context)

    @method_decorator(user_passes_test(must_be_master))
    def post(self, request, *args, **kwargs):

        reader = HarnessChartReader()
        reader.load_file(request.FILES['harness_chart'])
        reader.read_file_chart()

        harness_number = request.POST['harness_number']

        harness = Harness(harness_number=harness_number)
        harness.save()
        HarnessChart.save_from_dataframe(
            harness_dataframe=reader.get_dataframe(),
            harness_number=harness_number
        )
        

        return redirect('komax_app:harnesses')

@method_decorator(user_passes_test(must_be_master), name='dispatch')
class EquipmentListView(LoginRequiredMixin, View):
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

    @method_decorator(permission_required('komax_app.view_komax'))
    @method_decorator(permission_required('komax_app.view_kappa'))
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

class LaboriousnessListView(LoginRequiredMixin, View):
    template_name = 'komax_app/laboriousness.html'

    @method_decorator(permission_required('komax_app.view_laboriousness'))
    def get(self, request, *args, **kwargs):
        laboriousness = Laboriousness.objects.all()

        if len(laboriousness) == 0:
            fulfill_time()

        
        context = {
            'actions': laboriousness,
        }

        return render(request, self.template_name, context)

    @method_decorator(user_passes_test(must_be_master))
    def post(self, request, *args, **kwargs):
        """
        add or change laboriousness

        :param request:
        :param args:
        :param kwargs:
        :return:
       """
class LaboriousnessEditView(UpdateView, LoginRequiredMixin):
    model = Laboriousness
    fields = ['action', 'time']
    template_name = 'komax_app/laboriousness_delete.html'

    def get_object(self, queryset=None):
        obj = self.model.objects.get(action=self.kwargs['action'])
        return obj

class LaboriousnessDeleteView(LoginRequiredMixin,DeleteView):
    model = Laboriousness
    success_url = '/laboriousness/'
    def get_object(self, queryset=None):
        obj = self.model.objects.get(action=self.kwargs['action'])
        return obj

class LaboriousnessCreateView(LoginRequiredMixin, CreateView):
    model = Laboriousness
    fields = ['action', 'time']
    template_name = 'komax_app/laboriousness_create_form.html'

@method_decorator(user_passes_test(must_be_master), name='dispatch')
class KomaxTaskSetupView(LoginRequiredMixin, View):
    template_name = 'komax_app/task_setup.html'

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

class KomaxTaskListView(LoginRequiredMixin, PermissionRequiredMixin, View):
    template_name = 'komax_app/komax_tasks.html'
    permission_required = 'komax_app.view_komaxtask'

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

class KomaxEditView(LoginRequiredMixin, PermissionRequiredMixin, generic.UpdateView):
    model = Komax
    form_class = KomaxEditForm
    context_object_name = 'komaxes'
    template_name = 'komax_app/komaxes_edit.html'
    permission_required = (
        'komax_app.add_komax',
        'komax_app.change_komax',
        'komax_app.delete_komax',
        'komax_app.view_komax'
    )
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

def stop_task_on_komax(request, task_name, komax, *args, **kwargs):
    worker = get_object_or_404(Worker, user=request.user)
    if int(komax) != int(worker.current_komax.number):
        return Http404()

    komax_task = get_object_or_404(KomaxTask, task_name=task_name)
    komax = worker.current_komax
    stop_komax_task_on_komax(komax, komax_task)
    if TaskPersonal.objects.filter(komax=komax, loaded=True, komax_task=komax_task).exists():
        KomaxOrder.objects.create(komax_task=komax_task, komax=komax, status="Requested")
    else:
        pass

    return redirect('komax_app:user_account')

@method_decorator(ensure_csrf_cookie, name='dispatch')
class KomaxClientView(View):

    def get(self, request, *args, **kwargs):
        komax_number = int(request.GET['komax-number']) if 'komax-number' in request.GET else None
        if komax_number is not None:
            request.session['komax-number'] = komax_number
        return JsonResponse(dict())

    @method_decorator(csrf_exempt)
    def post(self, request, *args, **kwargs):
        params = dict()
        komax_number = request.session['komax-number']
        try:
            worker = Worker.objects.get(current_komax__number=komax_number)
        except Worker.DoesNotExist:
            worker = None
        status = int(request.POST['status']) if 'status' in request.POST else None #Статус сообщения комакса

        if komax_number is not None and status is not None and worker:
            if status == 1:
                position_info = request.POST['position'] if 'position' in request.POST else None
                if position_info is not None:
                    create_update_komax_status(komax_number, position_info) #KomaxStatus update

                komax_order = get_komax_order(komax_number)
                if komax_order is not None:
                    if komax_order.status == 'Requested':
                        params = {
                            'status': 2,
                            'text': komax_order.status,
                        }
                    elif komax_order.status == 'Received':
                        new_komax_task_df = get_task_to_load(komax_number)
                        if new_komax_task_df is not None:
                            params = {
                                'status': 2,
                                'task': new_komax_task_df.to_dict(),
                                'text': komax_order.status
                            }
            elif status == 2:
                text = request.POST['text'] if 'text' in request.POST else None
                task = json.loads(request.POST['task']) if 'task' in request.POST else None
                if text is not None and text == 'Requested' and task is not None:
                    save_komax_task_personal(komax_number, task, worker)
            elif status == 3:
                delete_komax_status(komax_number)
                delete_komax_order()

        return JsonResponse(params)

class KomaxTaskView(LoginRequiredMixin, View):
    model = KomaxTask
    template_name = 'komax_app/task_view.html'
    def get(self, request, task_name, *args, **kwargs):
        worker = get_object_or_404(Worker, user=request.user)
        task = get_object_or_404(self.model, task_name=task_name)
        harnesses = task.harnesses.all()
        status = 'success'
        komaxes_time = task.komaxes.all()
        final_alloc = {komax_time.komax.number: komax_time.time for komax_time in komaxes_time}
        task_kappas = task.kappas
        exceeds_shift = False

        if task_kappas is None:
            kappas = []
        else:
            kappas = [task_kappas]


        for key, item in final_alloc.items():
            if final_alloc[key] / 3600 > task.shift:
                exceeds_shift = True
            final_alloc[key] = seconds_to_str_hours(final_alloc[key])
        komax_num = request.session.get('komax', None)
        if komax_num == None:
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
        else:
            final_alloc_op=dict()
            final_alloc_op[int(komax_num)]=final_alloc[int(komax_num)]
            context = {
                'task': task,
                'harnesses': harnesses,
                'alloc': final_alloc_op,
                'harness_amount': 12 // len(harnesses),
                'komaxes_amount': 12 // len(final_alloc),
                'exceeds_shift': exceeds_shift,
                'status': status,
                'kappas': kappas,
            }

        return render(request, self.template_name, context=context)

    def post(self, request, task_name, *args, **kwargs):
        komax_task = get_object_or_404(KomaxTask, task_name=task_name)
        ordered_komax_task_objs = OrderedKomaxTask.objects.filter(komax_task=komax_task)

        if len(ordered_komax_task_objs):
            ordered_komax_task_objs.delete()
        else:
            ordered_komax_task_objs = [
                OrderedKomaxTask(komax_task=komax_task, komax=komax_i) for komax_i in komax_task.komaxes.all()
            ]
            OrderedKomaxTask.objects.bulk_create(ordered_komax_task_objs)
        return redirect('komax_app:task_view', task_name=task_name)

@login_required
@user_passes_test(must_be_master)
def get_harness_chart_view(request, harness_number):
    harness_chart_query = HarnessChart.objects.filter(harness__harness_number=harness_number)
    if len(harness_chart_query):
        harness_chart_df = read_frame(harness_chart_query)
    else:
        return Http404("Harness not found")

    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    )
    response['Content-Disposition'] = 'attachment; filename={}.xlsx'.format(harness_number)

    harness_chart_file = OutProcess(harness_chart_df)
    workbook = harness_chart_file.get_harness_chart_xl()
    workbook.save(response)

    return response

# @login_required
# @permission_required('komax_app.view_komaxtask')
def get_personal_task_view_komax(request, task_name, komax):
    komax_obj = get_object_or_404(Komax, number=komax)
    tasks_obj = get_object_or_404(KomaxTask, task_name=task_name)
    task_pers_df = read_frame(TaskPersonal.objects.filter(komax_task=tasks_obj, komax=komax_obj))

    task_pers_df.sort_values(
        by=['id'],
        ascending=True,
        inplace=True,
    )

    task_pers_df.drop(labels='worker', axis='columns', inplace=True)
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

# @login_required
# @user_passes_test(must_be_master)
def get_general_task_view(request, task_name):
    task_pers_df = read_frame(TaskPersonal.objects.filter(komax_task=get_object_or_404(KomaxTask, task_name=task_name)))

    task_pers_df.sort_values(
        by=['id'],
        ascending=True,
        inplace=True,
    )

    task_pers_df.drop(labels='worker', axis='columns', inplace=True)
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
    ws = workbook.active
    workbook.save(response)

    return response

# @login_required
# @user_passes_test(must_be_master)
def get_personal_task_view_kappa(request, task_name, kappa):
    komax_task_obj = get_object_or_404(KomaxTask, task_name=task_name)

    kappa_task_pers_df = read_frame(TaskPersonal.objects.filter(komax_task=komax_task_obj, kappa=komax_task_obj.kappas))

    kappa_task_pers_df.sort_values(
        by=['id'],
        ascending=True,
        inplace=True,
    )
    kappa_task_pers_df.drop(labels='worker', axis='columns', inplace=True)
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
    workbook = out_file.get_kappa_task_xl()
    workbook.save(response)

    return response

# @login_required
# @user_passes_test(must_be_master)
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

# @login_required
# @user_passes_test(must_be_master)
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

@login_required
@user_passes_test(must_be_master)
def harness_delete(request, harness_number):
    harness_to_delete = Harness.objects.filter(harness_number=harness_number)
    if len(harness_to_delete) > 0:
        harness_to_delete.delete()
    
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

def harness_chart_view(request, harness_number):
    harness_chart_objs = HarnessChart.objects.filter(harness__harness_number=harness_number)
    if len(harness_chart_objs):
        context = {
            'harness_number': harness_number,
            'positions': harness_chart_objs
        }
    
        return render(request, 'komax_app/chart_view.html', context)
    else:
        return Http404("Harness not found")

class MainPageKomaxAppView(View):
    template_name = 'komax_app/main_page.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('komax_app:user_account')

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
        return render(request, self.template_name, context=context)

    def post(self, request, *args, **kwargs):
        return

def index(request):
    return render(request, 'komax_app/index.html', context={"name" : "a"})
