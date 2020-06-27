from django.urls import path
from . import views

app_name = 'komax_app'

urlpatterns = [
    # main
    path('', views.MainPageKomaxAppView.as_view(), name='komax_app_view'),

    # komax api
    path('api/v1/komax/', views.KomaxClientView.as_view(), name='komax_client'),

    # tasks
    path('tasks/', views.TasksView.as_view(), name='tasks_view'),
    path('account/', views.WorkerAccountView.as_view(), name='user_account'),
    path('tasks/setup/', views.KomaxTaskSetupView.as_view(), name='task_setup'),
    path('tasks/<str:task_name>/', views.KomaxTaskView.as_view(), name='task_view'),
    path('tasks/<str:task_name>/delete/', views.delete_task, name='delete_task'),
    path('tasks/<str:task_name>/stop', views.stop_komax_task, name='stop_task'),
    path('tasks/<str:task_name>/stop/<str:komax>/', views.stop_task_on_komax, name='stop_task_on_komax'),
    path('tasks/<str:task_name>/get_task/', views.get_general_task_view, name='get_task'),
    path('tasks/<str:task_name>/get_task_komax/<str:komax>/',
            views.get_personal_task_view_komax, name='get_spec_task'),
    path('tasks/<str:task_name>/get_task_kappa/<str:kappa>/',
            views.get_personal_task_view_kappa, name='get_spec_task_kappa'),
    path('tasks/<str:task_name>/get_ticket_komax/<str:komax>/',
            views.get_komax_ticket_view, name='get_ticket_view'),
    path('tasks/<str:task_name>/get_ticket_kappa/<str:kappa>/',
         views.get_kappa_ticket_view, name='get_kappa_ticket_view'),
    path('tasks/<str:task_name>/send_task/', views.send_task_to_worker,
                name='send_komax_task'),
    path('tasks/<task_name>/load_task/', views.load_task_to_komax, name='load_komax_task'),

    # harnesses
    path('harnesses/', views.HarnessesListView.as_view(), name='harnesses'),
    path('harnesses/<str:harness_number>', views.harness_chart_view, name='harness_chart'),
    path('harnesses/<str:harness_number>/delete/', views.harness_delete, name='delete_harness'),
    path('harnesses/<str:harness_number>/download/', views.get_harness_chart_view, name='download_harness'),

    # komaxes
    path('komaxes/', views.EquipmentListView.as_view(), name='komaxes'),

    # laboriousness
    path('laboriousness/edit/<str:action>/delete/', views.LaboriousnessDeleteView.as_view(), name='laboriousness-delete'),
    path('laboriousness/create/', views.LaboriousnessCreateView.as_view(), name='laboriousness-create'),
    path('laboriousness/edit/<str:action>', views.LaboriousnessEditView.as_view(), name='laboriousness-edit'),
    path('laboriousness/', views.LaboriousnessListView.as_view(), name='laboriousness'),

    # others
    path('komax_tasks/', views.KomaxTaskListView.as_view(), name='komax_task_list'),
    path('komax_terminals/', views.KomaxTerminalsListView.as_view(), name='komax_terminals_list'),
    path('komax_seals/', views.KomaxSealsListView.as_view(), name='komax_seals_list')
]
